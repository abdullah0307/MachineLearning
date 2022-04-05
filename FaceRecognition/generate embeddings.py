import cv2
import face_recognition
import os

known_names = []
known_enc = []

path = r'RegisteredFaces'
images = os.listdir(path)

for image in images:
    img = cv2.imread(os.path.join(path, image))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)
    known_names.append(image)
    known_enc.append(encodings[0])

import pickle
pickle.dump(known_names, open("name.pickle", 'wb'))
pickle.dump(known_enc, open("enc.pickle", 'wb'))
