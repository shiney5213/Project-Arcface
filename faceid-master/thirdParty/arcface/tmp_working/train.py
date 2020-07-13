from src.arcface.model import Backbone, Arcface, MobileFaceNet, l2_norm
from src.arcface.utils import seperate_bn_paras
from src.arcface.data_loader import FaceLoader

import torch
from torch import optim

from tqdm import tqdm
from matplotlib import pyplot as plt
plt.switch_backend('agg')

from PIL import Image
from torchvision import transforms as transforms
from torch.nn import CrossEntropyLoss

import math
import bcolz

import os

class Trainer(object):
    def __init__(self, _dataloader, embedding_size=512):
        
        print('Trainer Initialization')

        # Learning Parameters
        self.step = 0 
        
        # CUDA, Model Setup.
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = MobileFaceNet(embedding_size).to(self.device)

        # Data Loader Setup. (Training, Validation)
        
        self.train_loader, self.valid_loader, self.class_num = _dataloader.get_loader()


        print('DataLoader Loaded !!\t Number of Classes: ', self.class_num)

        # Model Header.
        self.head = Arcface(embedding_size=embedding_size, classnum=self.class_num).to(self.device)

        paras_only_bn, paras_wo_bn = seperate_bn_paras(self.model)

        self.optimizer = optim.SGD([
                            {'params': paras_wo_bn[:-1], 'weight_decay': 4e-5},
                            {'params': [paras_wo_bn[-1]] + [self.head.kernel], 'weight_decay': 4e-4},
                            {'params': paras_only_bn}
                            ], lr = 1e-3, momentum = 0.9)

        print('Optimizer generated')

    def train(self, epochs, print_freq):
        self.model.train()
        
        train_loss = 0
        correct = 0
        total = 0
        
        for epoch in range(epochs):
            for imgs, labels in iter(self.train_loader):
                
                # Make Tensor
                imgs = imgs.to(self.device)
                labels = labels.to(self.device)
                #print('imgs.shape: ', imgs.shape)

                # Gradient Initialization
                self.optimizer.zero_grad()

                embeddings = self.model(imgs)
                #print('embeddings.shape: ', embeddings.shape)
                #print('label: ', labels)
                thetas = self.head(embeddings, labels)
                #print('theatas: ', thetas)
                loss = CrossEntropyLoss()
                output = loss(thetas, labels)

                output.backward()

                self.optimizer.step()
                
                if self.step % print_freq == 0 and self.step != 0:
                    print('epoch: ', epoch, 'step: ', self.step, 'loss: ', output.item())

                self.step += 1

            torch.save(self.head.state_dict(),'weights/' + str(epoch) +'.pth')                
            print('epoch: ', epoch, 'loss: ', output.item())



    # TODO
    # Validation Add
    # Save Graph 



