import socketio, base64
from detector import CameraDetector

CameraDetector.start()


# sio = socketio.Client()

# @sio.event
# def connect():
#     CameraDetector.start()

# sio.connect('http://localhost:5000')
# sio.wait()
