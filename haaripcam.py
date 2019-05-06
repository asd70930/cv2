import cv2
import threading
import time
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


fullbody_cascade  = cv2.CascadeClassifier("haarcascade_fullbody.xml")
upperbody_cascade = cv2.CascadeClassifier("haarcascade_upperbody.xml")
face_cascade      = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

url = 'rtsp://admin:admin@192.168.101.100/Media/stream2'
cap = cv2.VideoCapture(url)
ipcam = ipcamCapture(cap)
ipcam.start()
time.sleep(2)
while(True):
    frame = ipcam.getframe()
    cv2.putText(frame, "face count", (20, 20), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 255, 255), 2, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #fullbody  = fullbody_cascade.detectMultiScale(gray, 1.3, 5)
    #upperbody = upperbody_cascade.detectMultiScale(gray, 1.3, 5)
    faces     =face_cascade.detectMultiScale(gray, 1.3, 5)
    l = len(faces)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.putText(frame, str(l), (230, 20), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 255, 255), 2, 1)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()