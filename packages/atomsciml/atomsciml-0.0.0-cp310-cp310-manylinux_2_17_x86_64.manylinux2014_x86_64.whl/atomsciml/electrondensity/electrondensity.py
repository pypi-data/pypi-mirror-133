# ----------------------------------------------------------------------
# This problem can be classified into the Object Counting problem
# maybe we can refer to object counting problem in computer vision
# models like YOLO might give us some hints on how to solve thep roblem.
# ----------------------------------------------------------------------


# ------------------------------------------------------------------------
# Usage:
# from atomsciml.electrondensity.electrondensity import prepare_data, Task
# prepare_data("./electron-density-ml")
# task = Task("./electron-density-ml")
# task.run()
# ------------------------------------------------------------------------

import os
import os
import shutil
import time
import numpy as np

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
#import torchvision.transforms as transforms
#import torchvision.datasets as datasets
#import torch.nn.functional as F
from torch.utils.data import Dataset

from pymatflow.charge.chg_vasp import VaspCHG
from pymatflow.third import aflow as af

class ElectronDensityDataset(Dataset):
    """
    prividing training and validating dataset for ElectronDensityNet

    :param directory: the directory to store the dataset
    """
    def __init__(self, directory):
        self.directory = directory
        self.files = os.listdir(self.directory)
        
    def __getitem__(self, index):
        vaspchg = VaspCHG(os.path.join(self.directory, self.files[index], "CHGCAR.static"))
        
        #total_electrons = np.sum(vaspchg.data) / vaspchg.cell_volume * vaspchg.cell_volume_per_unit
        vaspchg.data = vaspchg.data / vaspchg.cell_volume * vaspchg.cell_volume_per_unit
        #

        natoms = len(vaspchg.structure.atoms)
        #return charge, label
        #label = np.arange(100)
        #label[:] = 0
        #label[natoms-1] = 1
        label = natoms
        return torch.Tensor([vaspchg.data]).float(), torch.tensor([label]).float() #torch.Tensor(label).long()

    def __len__(self):
        return len(self.files)



class ElectronDensityNet(nn.Module):
    """
    The electron density network is designed to map the Electron Density of
    one structure to the number of electrons, using 3D Convolutiional Neural
    Network.

    :param pretrained: whethe the model is pretrained.
    """

    def __init__(self, pretrained=False):
        super(ElectronDensityNet, self).__init__()

        self.conv1 = nn.Conv3d(1, 32, kernel_size=(3, 3, 3), padding=(1, 1, 1))
        #self.pool1 = nn.MaxPool3d(kernel_size=(1, 2, 2), stride=(1, 2, 2))
        self.pool1 = nn.AvgPool3d(kernel_size=(3, 3, 3), stride=(2, 2, 2))
        
        self.conv2 = nn.Conv3d(32, 64, kernel_size=(3, 3, 3), padding=(1, 1, 1))
        #self.pool2 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2))
        self.pool2 = nn.AvgPool3d(kernel_size=(3, 3, 3), stride=(2, 2, 2))

        #self.fc3 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(64, 512)
        self.fc4 = nn.Linear(512, 1)

        self.dropout = nn.Dropout(p=0.5)

        self.relu = nn.ReLU()
        self.leaky_relu = nn.LeakyReLU(0.01)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):

        #x = self.relu(self.conv1(x))
        #x = self.leaky_relu(self.conv1(x))
        x = self.sigmoid(self.conv1(x))
        x = self.pool1(x)

        #x = self.relu(self.conv2(x))
        #x = self.leaky_relu(self.conv2(x))
        x = self.sigmoid(self.conv2(x))
        x = self.pool2(x)
        
        #print(x.shape) # (batch_size, channels:64, depth, height, width)
        x = x.sum((2, 3, 4))
        x = self.relu(self.fc3(x))
        x = self.dropout(x)

        natoms = self.fc4(x)
        #print(natoms)
        return natoms




def prepare_data(directory="./electron-density-ml"):
    aurls_train = []
    result = af.search("species((Ba:Ca),Ti, O),nspecies(3),Egap(2*,*5),energy_cell")
    #print(len(result))
    for item in result:
        aurls_train.append(item["aurl"])

    aurls_val = []
    result = af.search("species((Pb:Bi),Ti, O),nspecies(3),Egap(2*,*5),energy_cell")
    #print(len(result))
    for item in result:
        aurls_val.append(item["aurl"]) 
        
    for aurl in aurls_train:
        print(aurl)
        if os.path.exists(os.path.join(directory, "train/%s" % aurl.split("/")[-1])):
            continue
        af.download_chgcar_from_aurl(aurl, directory=os.path.join(directory, "train/%s" % aurl.split("/")[-1]))
    for aurl in aurls_val:
        print(aurl)
        if os.path.exists(os.path.join(directory, "val/%s" % aurl.split("/")[-1])):
            continue
        af.download_chgcar_from_aurl(aurl, directory=os.path.join(directory, "/val/%s" % aurl.split("/")[-1]))


def adjust_learning_rate(learning_rate, optimizer, epoch):
    """
    Notes:
        After 100 and 150 epochs, set the learning rate to 
        the value of decaying initial LR by 10
    """

    learning_rate = learning_rate * (0.1 ** (epoch // 100)) * (0.1 ** (epoch // 150))
    
    for param_group in optimizer.param_groups:
        param_group['lr'] = learning_rate


class AverageMeter(object):
    """
    Notes:
        Computes and stores the average and current value
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def accuracy(output, target, topk=(1,)):
    """
    Notes:
        Computes the precision@k for the specified values of k
    """
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res


def save_checkpoint(state, is_best, filename='checkpoint.pth.tar'):
    """Saves checkpoint to disk"""
    name = "electrons"
    directory = "runs/%s/"%(name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = directory + filename
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, 'runs/%s/'%(name) + 'model_best.pth.tar')


def train(train_loader, model, criterion, optimizer, epoch, print_freq):
    """
    Train for one epoch on the training set
    """
    batch_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()
    # switch to train mode
    model.train()

    end = time.time()
    for i, (input, target) in enumerate(train_loader):
        #target = target.cuda(async=True)
        target = target.cuda()
        input = input.cuda()
        input_var = torch.autograd.Variable(input)
        target_var = torch.autograd.Variable(target)

        # compute output
        output = model(input_var)
        print(output)
        print(target)
        loss = criterion(output, target_var)

        # measure accuracy and record loss
        prec1 = accuracy(output.data, target, topk=(1,))[0]
        #losses.update(loss.data[0], input.size(0))
        losses.update(loss.item(), input.size(0))
        #top1.update(prec1[0], input.size(0))
        top1.update(prec1.item(), input.size(0))

        # compute gradient and do SGD step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        if i % print_freq == 0:
            print('Epoch: [{0}][{1}/{2}]\t'
                'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                'Prec@1 {top1.val:.3f} ({top1.avg:.3f})'.format(
                    epoch, i, len(train_loader), batch_time=batch_time,
                    loss=losses, top1=top1))
    # log to TensorBoard
    #if tensorboard:
    #    log_value('train_loss', losses.avg, epoch)
    #    log_value('train_acc', top1.avg, epoch)


def validate(val_loader, model, criterion, epoch, print_freq):
    """
    Perform validation on the validation set
    """
    batch_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()

    # switch to evaluate mode
    model.eval()

    end = time.time()
    for i, (input, target) in enumerate(val_loader):
        #target = target.cuda(async=True)
        target = target.cuda()
        input = input.cuda()
        input_var = torch.autograd.Variable(input, volatile=True)
        target_var = torch.autograd.Variable(target, volatile=True)

        # compute output
        output = model(input_var)
        loss = criterion(output, target_var)

        print("Validate:\n")
        print("output: ", output)
        print("\n")
        print("target: ", target_var)
        print("\n")
        # measure accuracy and record loss
        prec1 = accuracy(output.data, target, topk=(1,))[0]
        #losses.update(loss.data[0], input.size(0))
        losses.update(loss.item(), input.size(0))
        #top1.update(prec1[0], input.size(0))
        top1.update(prec1.item(), input.size(0))

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        if i % print_freq == 0:
            print('Test: [{0}/{1}]\t'
                'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                'Prec@1 {top1.val:.3f} ({top1.avg:.3f})'.format(
                    i, len(val_loader), batch_time=batch_time, loss=losses,
                    top1=top1))

    print(' * Prec@1 {top1.avg:.3f}'.format(top1=top1))
    # log to TensorBoard
    #if tensorboard:
    #    log_value('val_loss', losses.avg, epoch)
    #    log_value('val_acc', top1.avg, epoch)
    return top1.avg


class Task:
    """
    Notes:
        Designed to train and validate the ElectronDensityNet

    :param directory: directory where train data is stored.

    Usage:
        from atomsciml.electrondensity.electrondensity import prepare_data, Task
        prepare_data("./electron-density-ml")
        task = Task("./electron-density-ml")
        task.run()
    """
    def __init__(self, directory):
        self.train_dir = os.path.join(directory, "train")
        self.val_dir = os.path.join(directory, "val")
        self.batch_size = 1
        self.kwargs = {'num_workers': 1, 'pin_memory': True}
        self.learning_rate = 0.001
        self.momentum = 0.3
        self.weight_decay = 1.0e-4
        self.print_freq = 10

        self.train_loader = torch.utils.data.DataLoader(
            ElectronDensityDataset(directory=self.train_dir),
            batch_size=self.batch_size, shuffle=True, **self.kwargs
        )
        self.val_loader = torch.utils.data.DataLoader(
            ElectronDensityDataset(directory=self.val_dir),
            batch_size=self.batch_size, shuffle=True, **self.kwargs
        )

        # create model
        self.model = ElectronDensityNet()

        # get the number of model parameters
        print('Number of model parameters: {}'.format(
            sum([p.data.nelement() for p in self.model.parameters()])))

        # for training on multiple GPUs. 
        # Use CUDA_VISIBLE_DEVICES=0,1 to specify which GPUs to use
        # model = torch.nn.DataParallel(model).cuda()
        self.model = self.model.cuda()

        cudnn.benchmark = True

        # define loss function (criterion) and pptimizer
        #criterion = nn.CrossEntropyLoss().cuda()
        self.criterion = nn.MSELoss().cuda()
        self.optimizer = torch.optim.SGD(self.model.parameters(), self.learning_rate,
                                    momentum=self.momentum,
                                    nesterov=True,
                                    weight_decay=self.weight_decay)            

    def run(self, epochs=25):
        best_prec1 = 0
        for epoch in range(epochs):
            adjust_learning_rate(self.learning_rate, self.optimizer, epoch)

            # train for one epoch
            train(self.train_loader, self.model, self.criterion, self.optimizer, epoch, self.print_freq)
            
            # evaluate on validation set
            prec1 = validate(self.val_loader, self.model, self.criterion, epoch, self.print_freq)
            # remember best prec@1 and save checkpoint
            is_best = prec1 > best_prec1
            best_prec1 = max(prec1, best_prec1)
            save_checkpoint({
                'epoch': epoch + 1,
                'state_dict': self.model.state_dict(),
                'best_prec1': best_prec1,
            }, is_best)
        print('Best accuracy: ', best_prec1)


