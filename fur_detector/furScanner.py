import socketio, time
import cv2 as cv
from coreFunc.streaming import Vision
from coreFunc.controller import Mobility
from coreFunc.genConfig import create_config

sio = socketio.Client()
mobility = Mobility()
prevDir = 0
endStream = False


def streamingFrame(eventName):
	vision = Vision()
	ret, vision.frame = vision.captureFrame()
	sio.emit(eventName, vision.getFrameBytes().decode('utf8'))
	vision.camera.release()

@sio.event
def connect():
	print('[CONNECTED] server connected')
	

@sio.event
def requestVaccumData():
	deviceConfig = create_config()
	sio.emit('authenticateVaccum', deviceConfig)

@sio.event
def startScanner(data):
	global endStream
	if data:
		endStream = False
		streamingFrame('furDetection')
	else:
		endStream = True

@sio.event()
def startStreaming():
	streamingFrame('initFrame')

@sio.event()
def manualMove(data):
	if data == 'forward':
		mobility.moveForward()
	elif data == 'backward':
		mobility.moveBackward()
	elif data == 'left':
		mobility.moveLeft()
	elif data == 'right':
		mobility.moveRight()
	elif data == 'stop':
		mobility.stop()


@sio.event
def controlRequest(data):
	global prevDir
	mobility.stop()
	if (data['status'] == 200 and 
	 	data['frameLocation'] != prevDir):
		if data['frameLocation'] == 1:
			mobility.moveLeft()
		if data['frameLocation'] == 0:
			mobility.stop()
		if data['frameLocation'] == 2:
			mobility.moveRight()

		prevDir = data['frameLocation']
	
	if endStream == False:
		streamingFrame('furDetection')
	else:
		print('scanner stopped')

sio.connect('http://192.168.1.21:3055')
sio.wait()
	