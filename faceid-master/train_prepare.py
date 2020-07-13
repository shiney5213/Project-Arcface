import os
import face_src.prepare as prepare

base_dir = 'C:/work_datasets/vgg'

def start():
    print("Started")
    img_root = os.path.join(base_dir,"train")
    align_root = os.path.join(base_dir,"aligned")
    if not os.path.isdir(align_root) :
        os.mkdir(align_root)

    prepare.make_aligned_dataset(img_root, align_root)

if __name__ == '__main__' :
    start()