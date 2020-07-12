from face_src.model import Backbone, Arcface, MobileFaceNet, l2_norm
from face_src.utils import seperate_bn_paras
from face_src.data_loader import faceLoader

import torch
from torch import optim

from tqdm import tqdm

from PIL import Image
from torchvision import transforms as transforms
from torch.nn import CrossEntropyLoss
from torch.optim.lr_scheduler import StepLR
import torch.nn as nn

import math
import bcolz
# import visdom
import numpy as np

import os

class faceTrainer:
    def __init__(self, device, dataloader, embedding_size=512):
        
        print('Trainer Initializing')

        # Learning Parameters
        self.step = 0 
        
        # CUDA, Model Setup.
        self.device = device

        self.model = MobileFaceNet(embedding_size)

        # multi GPU
        if torch.cuda.device_count() > 1:
            print("CUDAs", torch.cuda.device_count(), "GPUs!")
            # 이거 쓰면 서버 터짐... 우분투로 다시 설치할 필요 있음
            # self.model = nn.DataParallel(self.model)
        
        self.model = self.model.to(self.device)

        # Data Loader Setup. (Training, Validation)
        self.train_loader, self.class_num = dataloader.get_loader()

        # Model Header.
        self.head = Arcface(embedding_size=embedding_size, classnum=self.class_num).to(self.device)
        '''
        paras_only_bn, paras_wo_bn = seperate_bn_paras(self.model)
        self.optimizer = optim.SGD([
                            {'params': paras_wo_bn[:-1], 'weight_decay': 4e-5},
                            {'params': [paras_wo_bn[-1]] + [self.head.kernel], 'weight_decay': 4e-4},
                            {'params': paras_only_bn}
                            ], lr = 0.1, momentum = 0.9)
        '''
        self.optimizer = optim.SGD(self.model.parameters(), lr=1e-1, weight_decay=5e-4)
        self.scheduler = StepLR(self.optimizer, step_size=10, gamma=0.1)
        self.loss = CrossEntropyLoss()

    def train(self, epochs, print_freq):

        self.model.train()
        
        for epoch in range(epochs):
            
            self.step = 0
            train_loss = 0
            correct = 0
            total = 0

            for imgs, labels in iter(self.train_loader):
                
                # Make Tensor
                imgs = imgs.to(self.device)
                labels = labels.to(self.device)
                #print('imgs.shape: ', imgs.shape)

                # Gradient Initialization
                self.optimizer.zero_grad()

                embeddings = self.model(imgs)
                thetas = self.head(embeddings, labels)
                
                output = self.loss(thetas, labels)
                output.backward()
                train_loss += output.item()

                self.optimizer.step()
                
                if self.step % print_freq == 0 and self.step != 0:
                    print('epoch: ', epoch, 'step: ', self.step, 'loss: ', output.item())

                self.step += 1

            loss_avg = train_loss/len(self.train_loader)
            if not os.path.exists('../../data/weights_lr') :
                os.makedirs('../../data/weights_lr')
            torch.save(self.head.state_dict(),'../../data/weights1_lr' + str(epoch) +'_'+str(loss_avg)+'.pth')
            print('epoch: ', epoch, 'loss avg: ', loss_avg)

            self.scheduler.step()
