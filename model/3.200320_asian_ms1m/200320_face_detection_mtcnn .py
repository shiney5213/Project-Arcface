from mtcnn import MTCNN
import cv2
import os 
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'


old_dir_path = '../../celebrity'
new_dir_path = '../../asian_align_112'

old_dir_list = os.listdir(old_dir_path)
print('dir 개수',len(old_dir_list))

detector = MTCNN()
for i , people_name in enumerate(old_dir_list):
    print(i, people_name)
    new_people_dir = os.path.join(new_dir_path, str(i+90000))
#     print(new_people_dir)
    try:
        os.mkdir(new_people_dir)
    except Exception as err:
        pass
        
    people_path = os.path.join(old_dir_path, people_name)
    old_file_list = os.listdir(people_path)
    for j, file in enumerate(old_file_list):
        old_file_path = os.path.join(people_path, file)
        
        original_image = cv2.imread(old_file_path, 1)
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
                try:
                    resize_image = cv2.resize(crop_image, dsize=(112,112), interpolation = cv2.INTER_AREA)
                    resize_image = cv2.cvtColor(resize_image, cv2.COLOR_RGB2BGR)
                    save_path = f"{new_dir_path}/{i+90000}/{i+90000}0{j}.jpg"
                    cv2.imwrite(save_path, resize_image)
                    print(f'olddir : {people_name}, newdir: {i+90000}, oldfile: {file}, newfile:{i+90000}0{j}.jpg')
                except Exception as err:
                    print(file,err)
					