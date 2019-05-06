import dlib
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

url = 'rtsp://user:password@IP/Media/stream2'
cap = cv2.VideoCapture(url)
ipcam = ipcamCapture(cap)
ipcam.start()
time.sleep(1)
detector = dlib.get_frontal_face_detector()
while(True):
    frame = ipcam.getframe()

    face_rects = detector(frame, 0)

    for i, d in enumerate(face_rects):
        x1 = d.left()
        y1 = d.top()
        x2 = d.right()
        y2 = d.bottom()

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
