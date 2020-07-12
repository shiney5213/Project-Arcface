from datetime import datetime
from PIL import Image
from face_src.faceRecognizer import faceRecognizer
from face_src.utils import *

import base64
import cv2
import io
# import json
import numpy as np
import os
import re
import shutil
import sys
import time
import torch

## Initialize
activate = True

face_database = 'face_database/'
face_temp = 'face_temp/'
mobilefacenet_path = "model_mobilefacenet.pth"
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

faceRecog = faceRecognizer(threshold=2.0, model_path=mobilefacenet_path, 
                                facebank_path=face_database, embedding_size=512, device=device)

## 1. controll group directory
def create_group(group_hash:str):
    make_dir(face_database+""+group_hash)
    print("create group dir", group_hash)

def remove_group(group_hash:str):
    print("remove group", group_hash)

## 2. regist face
def regist_with_align(img:Image, group_id:str, object_id:str, img_id:str):
    result_dict = {}
    global activate
    activate = False

    data_dir = face_database + group_id + '/' + object_id + '/'
    make_dir(data_dir)

    # TODO:agmentation image
    img = align_face(img)
    if img is None :
        result_dict['result'] = False
        result_dict['description'] = "face not found"
        return result_dict

    temp_dir = face_temp + group_id + '/' + object_id + '/'
    make_dir(temp_dir)
    img.save(temp_dir+img_id+".jpg")

    embedding = faceRecog.extract_feature(img)
    embedding = embedding.detach().cpu().numpy()
    
    np.save(data_dir + img_id + ".npy", embedding)
    
    result_dict['result'] = True
    result_dict['description'] = "calculation ok"
    activate = True
    return result_dict

## 3. identify face
def identify_with_align(img:Image, group_id:str, threshold=2.0, limit=10):
    global activate
    activate = False
    result_dict = {}

    img = align_face(img)
    if img is None :
        result_dict['result'] = False
        result_dict['description'] = "face not found"
        return result_dict

    temp_img_name = group_id + "_" + datetime.now().strftime('%Y-%m-%d_%H%M%S') + ".jpg"
    img.save(face_database + temp_img_name)

    result_dict['result'] = True
    result_dict['object_id_list'] = faceRecog.check_registration(img, group_id, threshold)["object_id_list"]
    
    while limit < len(result_dict['object_id_list']):
        del(result_dict['object_id_list'][-1])

    result_dict['count'] = len(result_dict['object_id_list'])
    activate = True
    
    return result_dict