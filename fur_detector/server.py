import base64, cv2 as cv, json
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, join_room
from werkzeug.utils import secure_filename
from detectorBot import TfLiteModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
sio = SocketIO(app, cors_allowed_origins='*')

imagePath = 'imageUpload'
model = TfLiteModel(model='custom_model_lite/detect.tflite',
                    label='custom_model_lite/labelmap.txt')

universalToken = 'pPKiKukNV18Gmi75jjxXDiw1JBWjssBX-GcsLNJTQwY'
devices = []

def readDeviceList():
    resultList = None
    with open('devices.json', 'r') as file:
        resultList = json.load(file)
        return resultList
    

def saveDeviceList(deviceList):
    with open('devices.json', 'w') as file:
        json.dump(deviceList, file)


def generateDetections(image):
    image = cv.imread(image)
    return model.detect_frame(image)

def checkDuplicateVaccum(id,list):
    if devices:
        for vaccum in list:
            if vaccum['device_id'] == id:
                return True
    return False    

def removeVaccum(id):
     if devices:
        for vaccum in devices:
            if vaccum['sessionId'] == id:
                devices.remove(vaccum)

@sio.event
def connect():
    print(f'[CONNECTED] User id: {request.sid}')
    sio.emit('requestVaccumData', include_self=True)


@sio.event
def authenticateVaccum(data):
    savedDevices = readDeviceList()
    if not savedDevices['devices']:
        if not checkDuplicateVaccum(data['device_id'],devices):
            devices.append(data)

    sio.emit('initVaccumList', devices, include_self=True)
    print(devices)

@sio.event
def vaccumUserAuth(data):
    global devices
    savedDevices = readDeviceList()
    data['device']['user'] = data['user']
    savedDevices['devices'] = [data['device']]
    saveDeviceList(savedDevices)

    devices = []
    print('application device connected')
    print(devices)

@sio.event
def initManualControl():
    print("Starting manual control")
    sio.emit('startStreaming')

@sio.event
def initFrame(data):
    sio.emit('viewFrame', data)
    
@sio.event
def initScanner(data):
    sio.emit('startScanner', data)


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
def requestManualMove(data):
    sio.emit('manualMove', data)

@sio.event
def disconnectVaccum(data):
    global devices
    savedDevices = readDeviceList()
    print('reaactivate')
    savedDevices['devices'] = []
    devices = [data]

    saveDeviceList(savedDevices)
    print(devices)

@sio.event
def disconnect():
    global devices
    print(f'[DISCONNECTED] User id: {request.sid}')
    devices = []
    sio.emit('initVaccumList', devices)
    print(f'Number of devices #{len(devices)}')

if __name__ == '__main__':
    sio.run(app, debug=True, host='0.0.0.0', port=3055)




