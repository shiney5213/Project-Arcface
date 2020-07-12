import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from PIL import Image

#------------------------

def euclidean_distance(a, b):
	x1 = a[0]; y1 = a[1]
	x2 = b[0]; y2 = b[1]
	return math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)))

# def detectFace(img, face_detector):
# 	faces = face_detector.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)    #1.3, 5

# 	print("found faces: ",len(faces))

# 	if len(faces) > 0:
# 		face = faces[0]
# 		x, y, w, h = face
# 		pad=30
# 		img = img[int(y-pad):int(y+h+pad), int(x-pad):int(x+w+pad)]

# 		return img #, img_gray
# 	else:
# 		return None #, img_gray

def cropFace(img, face_detector):
	faces = face_detector.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)    #1.3, 5

	print("found faces: ",len(faces))

	if len(faces) > 0:
		face = faces[0]
		x, y, w, h = face
		img = img[int(y):int(y+h), int(x):int(x+w)]

		return img #, img_gray
	else:
		return None #, img_gray
		#raise ValueError("No face found in the passed image ")

def alignFace(img, eye_detector, face_detector):
	if img is None:
		return None
	# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	

	eyes = eye_detector.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5, minSize=(20,20))
	print("found eyes: ",len(eyes))
	
	if len(eyes) >= 2:
		#--------------------
		#find the largest 2 eye

		base_eyes = eyes[:, 2]
		
		items = []
		for i in range(0, len(base_eyes)):
			item = (base_eyes[i], i)
			items.append(item)
		
		df = pd.DataFrame(items, columns = ["length", "idx"]).sort_values(by=['length'], ascending=False)
		
		eyes = eyes[df.idx.values[0:2]]
		
		#--------------------
		#decide left and right eye
		
		eye_1 = eyes[0]; eye_2 = eyes[1]
		
		if eye_1[0] < eye_2[0]:
			left_eye = eye_1
			right_eye = eye_2
		else:
			left_eye = eye_2
			right_eye = eye_1
		
		#--------------------
		#center of eyes
		
		left_eye_center = (int(left_eye[0] + (left_eye[2] / 2)), int(left_eye[1] + (left_eye[3] / 2)))
		left_eye_x = left_eye_center[0]; left_eye_y = left_eye_center[1]
		
		right_eye_center = (int(right_eye[0] + (right_eye[2]/2)), int(right_eye[1] + (right_eye[3]/2)))
		right_eye_x = right_eye_center[0]; right_eye_y = right_eye_center[1]

		#----------------------
		#rotation direction
		
		if left_eye_y > right_eye_y:
			point_3rd = (right_eye_x, left_eye_y)
			direction = -1 #rotate same direction to clock
			print("rotate to clock direction")
		else:
			point_3rd = (left_eye_x, right_eye_y)
			direction = 1 #rotate inverse direction of clock
			print("rotate to inverse clock direction")
		
		#--------------------
		#rotaion angle

		# cv2.circle(oneFace, point_3rd, 2, (255, 0, 0) , 2)
		
		# cv2.line(oneFace,right_eye_center, left_eye_center,(67,67,67),1)
		# cv2.line(oneFace,left_eye_center, point_3rd,(67,67,67),1)
		# cv2.line(oneFace,right_eye_center, point_3rd,(67,67,67),1)

		# cv2.imshow("draw0", oneFace)

		a = euclidean_distance(left_eye_center, point_3rd)
		b = euclidean_distance(right_eye_center, point_3rd)
		c = euclidean_distance(right_eye_center, left_eye_center)
		
		cos_a = (b*b + c*c - a*a)/(2*b*c)

		angle = np.arccos(cos_a)
		
		angle = (angle * 180) / math.pi

		print(f"angle={angle}")

		if direction == -1:
			angle = 90 - angle

		print(f"rotate angle={angle}")

		#--------------------
		#rotate

		new_img = Image.fromarray(img)
		return np.array(new_img.rotate(direction * angle))
		# return new_img.rotate(direction * angle)
	else:
		return None
#------------------------

def align_n_crop(image, face_detector, eye_detector):
	alignedFace = alignFace(image, eye_detector, face_detector)
	if not alignedFace is None:
		npImage = cropFace(alignedFace, face_detector)
		# return npImage
		if not npImage is None:
			return Image.fromarray(dst)

	return None


# face_detector = cv2.CascadeClassifier("D:/workspaces/beface/face-server/dl/src/faceutil/haarcascade_frontalface_default.xml")
# eye_detector  = cv2.CascadeClassifier("D:/workspaces/beface/face-server/dl/src/faceutil/haarcascade_eye.xml") 

# image_path = "./test.jpg"

# image = cv2.imread(image_path)
# alignedFace = alignFace(image, eye_detector, face_detector)

# if not alignedFace is None:
# 	cv2.imshow("algined", alignedFace)
# 	cv2.waitKey(0)
# 	# plt.imshow(alignedFace[:, :, ::-1])
# 	# plt.show()

# 	face = cropFace(alignedFace, face_detector)
# 	cv2.imshow("face", face)
# 	cv2.waitKey(0)
# 	# plt.imshow(face[:, :, ::-1])
# 	# plt.show()
    
# else:
# 	print("no faces")


''' test code
conda activate beface

d:

cd D:\workspaces\beface\face-server\dl\src\faceutil

python faceutils.py
'''