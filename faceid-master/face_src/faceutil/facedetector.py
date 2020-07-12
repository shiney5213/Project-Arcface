
import cv2

def crop_face_from_path(img_path) :
    print(f"face path={img_path}")
    img = cv2.imread(img_path)
    return crop_face(img)
    
def crop_face(img):
    # Convert into grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    face_detector = cv2.CascadeClassifier('D:/workspaces/beface/face-server/dl/src/faceutil/haarcascade_frontalface_default.xml')
    faces = face_detector.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4, minSize=(120,120))
    # Draw rectangle around the faces
    print(f"face count={len(faces)}")
    if len(faces) > 0:
        face_array = []
        pad = 30
        for (x, y, w, h) in faces:
            cropped_face = gray_img[y-pad : y+h+pad , x-pad : x+w+pad]
            face_array.append(cropped_face)
        return face_array
    else:
        return None
    # 
    #     # cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    #     return 


# D:/workspaces/beface/face-server/dl/src/test/kodonho/org.jpg
faces = crop_face_from_path('D:/workspaces/beface/face-server/dl/src/faceutil/test.jpg')

if not faces is None:
    c=0
    for face in faces :
        c+=1
        cv2.imshow("face{}".format(c), face)
    cv2.waitKey(0)
else:
    print("no face")

