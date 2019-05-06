from os import walk
from os.path import join
import face_recognition
import cv2
import numpy as np

img = cv2.imread('who.jpg')

mypath = "img/"
urlpath=[]
known_face_encodings=[]
known_face_names=[]
for root, dirs, files in walk(mypath):
  for f in files:
    fullpath = join(root, f)
    urlpath.append(fullpath)
print(urlpath)
count=0

for i in urlpath:
    locals()['face_image%s'%count]=face_recognition.load_image_file(i)
    locals()['face_encoding%s' % count]=face_recognition.face_encodings(locals()['face_image%s'%count])[0]
    known_face_encodings.append(locals()['face_encoding%s' % count])
    known_face_names.append(i.split('/')[-1].split('.')[0])

face_locations = []
face_encodings = []
face_names = []

face_locations = face_recognition.face_locations(img)
face_encodings = face_recognition.face_encodings(img, face_locations)

for face_encoding in face_encodings:
    # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown"

    # # If a match was found in known_face_encodings, just use the first one.
    # if True in matches:
    #     first_match_index = matches.index(True)
    #     name = known_face_names[first_match_index]

    # Or instead, use the known face with the smallest distance to the new face
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]

    face_names.append(name)


    for (top, right, bottom, left) in face_locations:
        # top *= 2
        # right *= 2
        # bottom *= 2
        # left *= 2

        # Draw a box around the face
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.rectangle(img, (left, bottom - 2), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, name, (left + 1, bottom - 1), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('frame', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

