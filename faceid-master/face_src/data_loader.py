import torch

from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision import transforms
from torch.utils.data.sampler import SubsetRandomSampler
from PIL import Image, ImageFile

import numpy as np
import cv2
import torch

class faceLoader:
    def __init__(self, data_root, batch_size, shuffle=True):
        self.data_root = data_root
        self.batch_size = batch_size
        self.shuffle = shuffle

    def get_loader(self, img_size=[112,112]):
        train_transforms = transforms.Compose([
            transforms.Resize(img_size),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])

        train_datasets = ImageFolder(self.data_root, train_transforms)
        train_loader = DataLoader(train_datasets, batch_size=self.batch_size, num_workers=4, pin_memory=True)

        num_classes = train_datasets[-1][1] + 1

        return train_loader, num_classes
