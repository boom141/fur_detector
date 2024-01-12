import socketio, time, random
import cv2 as cv
from coreFunc.streaming import Vision
from coreFunc.controller import Mobility
from coreFunc.genConfig import create_config

sio = socketio.Client()
mobility = Mobility()
prevDir = 0
endStream = False

def randomDelay():
	return random.randint(1,3)

def streamingFrame(eventName):
	vision = Vision()
	ret, vision.frame = vision.captureFrame()
	sio.emit(eventName, vision.getFrameBytes().decode('utf8'))
	vision.camera.release()

@sio.event
def connect():
	print('[CONNECTED] server connected')
	# streamingFrame('initRoaming')
	time.sleep(1)
	roaming()

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
def furFollower(data):
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

		mobility.moveForward()
		prevDir = data['frameLocation']
	
	if endStream == False:
		streamingFrame('furDetection')
	else:
		print('scanner stopped')


@sio.event
def roaming():
	while 1:
		mobility.moveBackward(0.5)
		
		move = random.randint(2,4)
		if move == 2:
			mobility.moveForward(randomDelay())
		elif move == 3:
			mobility.moveLeft(randomDelay())
		elif move == 4:
			mobility.moveRight(randomDelay())

		mobility.moveForward(randomDelay())

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
	