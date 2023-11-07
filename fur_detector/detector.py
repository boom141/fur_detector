import cv2 as cv
import socketio, random

sio = socketio.Client()
sio.connect('http://localhost:5000')

while 1:
    random_number = random.random()
    if random_number < 0.2:
        sio.emit('test', {'data':round(random_number,2)})
