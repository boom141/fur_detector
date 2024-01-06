import socketio, time
import cv2 as cv
from coreFunc.streaming import Vision
from coreFunc.controller import Mobility

sio = socketio.Client()
mobility = Mobility()
prevDir = 0

def mainLoop(eventName):
	vision = Vision()
	ret, vision.frame = vision.captureFrame()
	sio.emit(eventName, vision.getFrameBytes().decode('utf8'))
	vision.camera.release()
	print('captured frame')

@sio.event
def connect():
	print('[CONNECTED] server connected')
	mainLoop('furDetection')

@sio.event
def controlRequest(data):
	global prevDir
	mobility.stop()
	if (data['status'] == 200 and 
	 	data['frameLocation'] != prevDir):
		if data['frameLocation'] == 1:
			print('left')
			mobility.moveLeft()
		if data['frameLocation'] == 0:
			print('center')
			mobility.stop()
		if data['frameLocation'] == 2:
			print('right')
			mobility.moveRight()

		prevDir = data['frameLocation']
	
	mainLoop('furDetection')

sio.connect('http://192.168.1.13:3055')
sio.wait()
	