import face_recognition
import cv2
import threading
import time
import numpy as np
import tkinter as tk
import tkinter.filedialog
from os import walk
from os.path import join
import re

class ipcamCapture:
    def __init__(self, capture):
        self.Frame = []
        self.status = False
        self.isstop = False
        self.capture = capture

    def start(self):
        print('ipcam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
        self.isstop = True
        print('ipcam stopped!')

    def getframe(self):
        return self.Frame

    def getstatus(self):
        return self.status

    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()
        self.capture.release()

def GetImgEncode(imgpath, urlpath, known_face_encodings, known_face_names):
    urlpath = []
    known_face_encodings = []
    known_face_names = []
    try:
        for root, dirs, files in walk(imgpath):
            for f in files:
                fullpath = join(root, f)
                urlpath.append(fullpath)
    except Exception as e:
        print(e)
    count = 0
    for i in urlpath:
        try:
            locals()['face_image%s' % count] = face_recognition.load_image_file(i)
            locals()['face_encoding%s' % count] = face_recognition.face_encodings(locals()['face_image%s' % count])[0]
        except :
            print('you make a wrong picture',i)
            continue
        known_face_encodings.append(locals()['face_encoding%s' % count])
        #known_face_names.append(i.split('/')[-1].split('.')[0])
        name = i.split('/')[-1].split('.')[0]
        r1 = '[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        name = re.sub(r1, '', name)
        known_face_names.append(name)
        count +=1

    return (urlpath,known_face_encodings,known_face_names)

# Image save path
imgpath = "img/"

# Ipcam url
url = 'rtsp://admin:admin@192.168.101.100/Media/stream1'

# roi range
(x1, x2, y1, y2) = (200, 800, 300, 800)

urlpath = []
known_face_encodings = []
known_face_names = []

(urlpath, known_face_encodings, known_face_names) = GetImgEncode(imgpath, urlpath,
                                                                 known_face_encodings, known_face_names)
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
try:
    cap = cv2.VideoCapture(url)
except Exception as e:
    print(e)

getipcam = cap.isOpened()
if getipcam:
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
    ipcam = ipcamCapture(cap)
    ipcam.start()
    time.sleep(1)
else:
    print('Your ipcamer ip or rtps address could not found')
sameframe = True
while(getipcam):
    try:
        frame = ipcam.getframe()
    except:
        ipcam.stop()
        cv2.destroyAllWindows()
        break
    roiframe = frame[x1: x2, y1: y2]
    small_frame = cv2.resize(roiframe, (0, 0), fx=1, fy=1)
    rgb_small_frame = small_frame[:, :, ::-1]

    if sameframe:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name)
    sameframe = not sameframe
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # top *= 2
        # right *= 2
        # bottom *= 2
        # left *= 2
        # Draw a box around the face
        cv2.rectangle(roiframe, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.rectangle(roiframe, (left, bottom - 2), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(roiframe, name, (left + 1, bottom - 1), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('frame', roiframe)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        time.sleep(0.1)
        frame = ipcam.getframe()
        roiframe = frame[x1: x2, y1: y2]
        root = tk.Tk()
        root.withdraw()
        a = tkinter.filedialog.asksaveasfilename()
        if str(a) != '()' and str(a) != '':
            url = imgpath + a.split("/")[-1].split('.')[0]+'.jpg'
            cv2.imwrite(url, roiframe)
            (urlpath, known_face_encodings, known_face_names) = GetImgEncode(imgpath, urlpath, known_face_encodings, known_face_names)
        else:
            # print('cancel?')
            pass
    elif cv2.waitKey(5) & 0xFF == ord('q'):
        ipcam.stop()
        cv2.destroyAllWindows()
        break
