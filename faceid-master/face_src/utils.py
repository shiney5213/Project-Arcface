from datetime import datetime
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import io
from torchvision import transforms
import torch
import pdb
import cv2
import argparse
import os
import shutil

from face_src.align_trans import get_reference_facial_points, warp_and_crop_face
from thirdParty.mtcnn import detect_faces

facebank_transform = transforms.Compose([
    transforms.Resize([112,112]),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])

face_ref_points=[
    [30.29459953, 51.69630051],
    [65.53179932, 51.50139999],
    [48.02519989, 71.73660278],
    [33.54930115, 92.3655014],
    [62.72990036, 92.20410156],
]

def align_face(img):
    # input : pillow image
    bb, landmarks = detect_faces(img)
    
    num_faces = len(bb)
    
    if num_faces > 0 :
        face_point = bb[0]
        landmark = landmarks[0]

        # get largest one
        if num_faces > 1 :
            for i in range(len(bb)) :
                face_area = face_point[2] * face_point[3]
                bb_area = bb[i][2] * bb[i][3]
                if face_area < bb_area :
                    face_point = bb[i]
                    landmark = landmarks[i]

        face_img = img.crop((face_point[0], face_point[1], face_point[2], face_point[3]))
        cv_face_img = cv2.cvtColor(np.asarray(face_img), cv2.COLOR_RGB2BGR)

        # align image
        facial5points = [[landmark[j], landmark[j+5]] for j in range(5)]
        warped_face = warp_and_crop_face(np.array(img), facial5points, face_ref_points, crop_size=(112,112))

        face_image = Image.fromarray(warped_face)
        
        return face_image
    else :
        return None


def seperate_bn_paras(modules):
    if not isinstance(modules, list):
        modules = [*modules.modules()]
    paras_only_bn = []
    paras_wo_bn = []
    for layer in modules:
        if 'model' in str(layer.__class__):
            continue
        if 'container' in str(layer.__class__):
            continue
        else:
            if 'batchnorm' in str(layer.__class__):
                paras_only_bn.extend([*layer.parameters()])
            else:
                paras_wo_bn.extend([*layer.parameters()])
    return paras_only_bn, paras_wo_bn

def prepare_facebank(train_root, model, device):
    model.eval()

    embeddings = []
    names = ['Unknown']

    for path in train_root.iterdir():
        if path.is_file():
            continue
        else:
            embs = []
            for file in path.iterdir():
                if not file.is_file():
                    continue
                else:
                    try:
                        img = Image.open(file)
                    except:
                        continue
                    
                    with torch.no_grad():
                        emb = model(facebank_transform(img).to(device).unsqueeze(0))

        if len(embs) == 0:
            continue

        embedding = torch.cat(embs).mean(0, keepdim=True)
        embeddings.append(embedding)
        names.append(path.name)

    embeddings = torch.cat(embeddings)
    names = np.array(names)
    torch.save(embeddings, train_root+'/facebank.pth')
    np.save(train_root+'/names', names)
    return embeddings, names

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, help='IP address', default='183.98.140.226')
    parser.add_argument('--port', type=int, help='Port Number', default=3000)
    
    return parser.parse_args(argv)

def make_dir(input_path):
    try:
        if not(os.path.isdir(input_path)):
            os.makedirs(os.path.join(input_path))

    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory")
            raise

def remove_dir(input_path):
    try:
        if os.path.isdir(input_path):
            shutil.rmtree(input_path)
            return str('True')

    except OSError as e:
        if e.errno != errno.EEXIST:
            print('Failed to delete directory')
            return str('False')
def remove_file(input_path):
    try:
        os.remove(input_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            return str('False')

def set_imgID(object_root):
    file_list = os.listdir(object_root)
    
    #imgID = object_root + '/' + str(len(file_list)) + '.npy'
    return str(len(file_list))

def changeName(before,after):
    try:
        if os.path.isdir(before):
            os.rename(before,after)
            return str('True')
        else:
            return str('False')
    except:
        return str('False')

