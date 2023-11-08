import cv2 as cv
import socketio, random
import base64

sio = socketio.Client()
sio.connect('http://localhost:5000')

camera = cv.VideoCapture(0)
send_counter = 0

while 1:
    success, frame = camera.read()

    if not success:
        break
    
    image_buffer = cv.imencode('.jpg', frame)[1]
    image_data = base64.b64encode(image_buffer)

    sio.emit('manual_control', {'file': image_data})
    
    cv.imshow('fur detector', frame)
    
    if cv.waitKey(1) == ord('q'):
        break

camera.release()
cv.destroyAllWindows()


