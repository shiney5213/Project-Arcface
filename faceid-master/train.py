import torch

from face_src.trainer import faceTrainer
from face_src.data_loader import faceLoader


def start():
    print("Started")
    # data_root = "../../work_datasets/vgg/train"
    # batch_size = 64
    data_root = "./db/small_vgg/train"
    batch_size = 8
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    print("Data Loading")
    dataloader = faceLoader(data_root, batch_size, shuffle=True)
    trainer = faceTrainer(device, dataloader, embedding_size=512)
    print("Begin Training on", device)
    trainer.train(50, 100)

if __name__ == '__main__' :
    start()