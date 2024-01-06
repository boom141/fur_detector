import base64, cv2 as cv
from flask import Flask, request
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from coreFunc.detectorBot import TfLiteModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app)

imagePath = 'imageUpload'
model = TfLiteModel(model='custom_model_lite/detect.tflite',
                    label='custom_model_lite/labelmap.txt')


def generateDetections(image):
    image = cv.imread(image)
    return model.detect_frame(image)


@sio.event
def connect():
    print(f'[CONNECTED] User id: {request.sid}')


@sio.event
def furDetection(dataBuffer):
    image_type = base64.b64decode(dataBuffer)

    filename = secure_filename('sample.jpg')
    with open( 'imageUpload/'+ filename, 'wb') as output:
        output.write(image_type)

    result = generateDetections(f'{imagePath}/{filename}')
    print(result)

    sio.emit('controlRequest', result, include_self=True)


@sio.event
def disconnect():
    print(f'[DISCONNECTED] User id: {request.sid}')



if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', port=3055)




