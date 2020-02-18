import mxnet as mx
from mxnet import ndarray as nd
import argparse
import pickle
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'eval'))
import lfw

parser = argparse.ArgumentParser(description='Package LFW images')
# general
parser.add_argument('--data-dir', default='../data/k-face/new_path/4.rename_test_align_112', help='')
parser.add_argument('--image-size', type=str, default='112,112', help='')
parser.add_argument('--output', default='../data/k-face/new_path/test-kface/kface.bin', help='path to save.')
args = parser.parse_args()
lfw_dir = args.data_dir
image_size = [int(x) for x in args.image_size.split(',')]
lfw_pairs = lfw.read_pairs(os.path.join('../data/k-face/new_path/test-kface', 'kface_pairs.txt'))
lfw_paths, issame_list = lfw.get_paths(lfw_dir, lfw_pairs, 'jpeg') # or jpg
lfw_bins = []
#lfw_data = nd.empty((len(lfw_paths), 3, image_size[0], image_size[1]))
i = 0
for path in lfw_paths:
  with open(path, 'rb') as fin:
    _bin = fin.read()
    lfw_bins.append(_bin)
    #img = mx.image.imdecode(_bin)
    #img = nd.transpose(img, axes=(2, 0, 1))
    #lfw_data[i][:] = img
    i+=1
    if i%1000==0:
      print('loading dataset', i)

with open(args.output, 'wb') as f:
  pickle.dump((lfw_bins, issame_list), f, protocol=pickle.HIGHEST_PROTOCOL)
