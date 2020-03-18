from mtcnn import MTCNN
import cv2
import os 
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'


old_dir = '../data/ordinary/lfw_10'
new_dir = '../data/ordinary/lfw_align_112'

old_dir_list = os.listdir(old_dir)

detector = MTCNN()
for root, dirs, files in os.walk(old_dir):
#     print(dirs)
    people_name = os.path.split(root)[1]
    print(people_name)
    new_people_dir = os.path.join(new_dir, people_name)
    try:
        os.mkdir(new_people_dir)
    except Exception as err:
        print(err)
        
    for i, file in enumerate(files):
        input_image_path = os.path.join(root, file)
        original_image = cv2.imread(input_image_path, 1)
        if original_image is not None:
            original_image= cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
            copy_image = original_image
#             face_locations = face_recognition.face_locations(original_image)
            face_locations = detector.detect_faces(original_image)
            
            for face_location in face_locations:
                # more bigger box size than ordinary box
                x, y, w, h = face_location['box']
                left = x
                top = y
                right = x + w
                bottom = y + h
                x_center= left + int(w/2)
                left = x_center - int(h/2)
                right = x_center + int( h/2)
                
                    
                crop_image = copy_image[top:bottom, left:right]
                # imshow('', crop_image)                
                resize_image = cv2.resize(crop_image, dsize=(112,112), interpolation = cv2.INTER_AREA)
                resize_image = cv2.cvtColor(resize_image, cv2.COLOR_RGB2BGR)
                save_path = f"{new_dir}/{people_name}/{file}"
                cv2.imwrite(save_path, resize_image)