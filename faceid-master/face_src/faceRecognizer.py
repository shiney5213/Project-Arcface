import cv2
from PIL import Image
import argparse
from pathlib import Path
import torch
from torchvision import transforms
import numpy as np
import os

from face_src.model import MobileFaceNet

class faceRecognizer:
    def __init__(self, threshold, model_path, facebank_path, embedding_size, device):
        self.threshold = threshold
        self.device = device
        
        # Model Loading
        self.model = MobileFaceNet(embedding_size).to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=device))
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize([112,112]),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
            ])
        
        self.facebank_path = facebank_path

        self.embeddings = None
        self.names = None
    
    def set_threshold(self, thresh):
        self.threshold = thresh
    

    def extract_feature(self, img):
        emb = self.model(self.transform(img).to(self.device).unsqueeze(0))
        return emb
    
    def make_facebank(self, group_id):
        names = []
        root_path = Path(self.facebank_path + group_id)
        embeddings = []

        for obj in root_path.iterdir():
            if obj.is_file():
                continue
            else:
                embs = []
                for file in obj.iterdir():
                    if not file.is_file():
                        continue
                    else:
                        emb = np.load(file)
                        emb = torch.from_numpy(emb).to(self.device)

                        embs.append(emb)

                if len(embs) == 0:
                    continue

                embedding = torch.cat(embs).mean(0, keepdim=True)
                embeddings.append(embedding)
                names.append(obj.name)

        if len(embeddings) > 0:
            embeddings = torch.cat(embeddings)
            names = np.array(names)
        
        return embeddings, names


    def check_registration(self, face, group_id, threshold):
        
        result_dict = {}
        result_dict['object_id_list'] = []
        
        # make feature
        face_tensor = self.transform(face).to(self.device)
        face_tensor = face_tensor.unsqueeze(0)
        emb = self.model(face_tensor)
        
        print('threshold: ', threshold)

        group_path = self.facebank_path + group_id

        if len(os.listdir(group_path)) > 0:
            facebank_embeddings, facebank_names = self.make_facebank(group_id) 

            diff = emb.unsqueeze(-1) - facebank_embeddings.transpose(1,0).unsqueeze(0)
            
            dist = torch.sum(torch.pow(diff, 2), dim=1)
            np_dist = np.squeeze(dist.detach().cpu().numpy(), axis=0)
            
            result_dist = np_dist[np.where(np_dist < threshold)]
            result_names = facebank_names[np.where(np_dist < threshold)]
            
            if result_dist.shape[0] > 0:
                for i in range(result_dist.shape[0]):
                    object_dict = {}
                    object_dict['object_id'] = result_names[i]
                    object_dict['distance'] = str(result_dist[i])
                    result_dict['object_id_list'].append(object_dict)
            else:
                object_dict = {}
                object_dict['object_id'] = "Unknown"
                object_dict['distance'] = "-1"
                result_dict['object_id_list'].append(object_dict)
        else:
            object_dict = {}
            object_dict['object_id'] = "Unknown"
            object_dict['distance'] = "-1"
            result_dict['object_id_list'].append(object_dict)
        
        result_dict['object_id_list'] = sorted(result_dict['object_id_list'], key=lambda result: (result['distance']))
        return result_dict
