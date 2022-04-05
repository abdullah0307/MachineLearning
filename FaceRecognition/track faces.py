import cv2
import face_recognition
import dlib
import pickle

known_names = pickle.load(open("name.pickle", 'rb'))
known_enc = pickle.load(open("enc.pickle", 'rb'))

face_detector = dlib.get_frontal_face_detector()
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray)

    if len(faces) > 0:
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            enc = face_recognition.face_encodings(rgb)[0]
            matches = face_recognition.compare_faces(known_enc, enc, tolerance=0.55)
            if True in matches:
                print(matches.index(True))

    else:
        cv2.putText(frame, "No Face", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
    cv2.imshow('', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
