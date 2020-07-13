import torch

from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision import transforms
from torch.utils.data.sampler import SubsetRandomSampler
from PIL import Image, ImageFile

import numpy as np
import cv2
import bcolz
import pickle
import torch
import mxnet as mx
from tqdm import tqdm

class FaceLoader:
    def __init__(self, root, mode, batch_size, valid_ratio, shuffle=True):
        self.root = root
        self.mode = mode
        self.batch_size = batch_size
        self.valid_ratio = valid_ratio
        self.shuffle = shuffle

        if self.valid_ratio > 0:
            self.valid = True
        else:
            self.valid = False

    def get_loader(self):
        train_transforms = transforms.Compose([
            transforms.Resize([112,112]),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])

        valid_transforms = transforms.Compose([
            transforms.Resize([112,112]),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
            ])

        train_datasets = ImageFolder(self.root, train_transforms)
        valid_datasets = ImageFolder(self.root, valid_transforms)
    
        num_train = len(train_datasets)
        indices = list(range(num_train))

        split = int(np.floor(self.valid_ratio * num_train))
        train_idx, valid_idx = indices[split:], indices[:split]
        
        train_sampler = SubsetRandomSampler(train_idx)
        valid_sampler = SubsetRandomSampler(valid_idx)
        
        train_loader = DataLoader(train_datasets, batch_size=self.batch_size, sampler=train_sampler, num_workers=4, pin_memory=True)

        valid_loader = DataLoader(valid_datasets, batch_size=self.batch_size, sampler=valid_sampler, num_workers=4, pin_memory=True)

        num_classes = train_datasets[-1][1] + 1

        return train_loader, valid_loader, num_classes
