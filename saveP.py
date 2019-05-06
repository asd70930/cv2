import cv2

vi = cv2.VideoCapture('test.mp4')

while(vi.isOpened()):
    _,frame = vi.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()