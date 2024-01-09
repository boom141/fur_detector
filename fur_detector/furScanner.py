import socketio, time
import cv2 as cv
from coreFunc.streaming import Vision
# from coreFunc.controller import Mobility
from coreFunc.genConfig import create_config

sio = socketio.Client()
# mobility = Mobility()
prevDir = 0
endStream = False

deviceConfig = create_config()

def streamingFrame(eventName):
	vision = Vision()
	ret, vision.frame = vision.captureFrame()
	sio.emit(eventName, vision.getFrameBytes().decode('utf8'))
	vision.camera.release()

@sio.event
def connect():
	print('[CONNECTED] server connected')
	# mainLoop('furDetection')

@sio.event
def requestVaccumData():
	sio.emit('authenticateVaccum', deviceConfig)


@sio.event()
def startStreaming():
	streamingFrame('initFrame')

# @sio.event
# def controlRequest(data):
# 	global prevDir
# 	mobility.stop()
# 	if (data['status'] == 200 and 
# 	 	data['frameLocation'] != prevDir):
# 		if data['frameLocation'] == 1:
# 			print('left')
# 			mobility.moveLeft()
# 		if data['frameLocation'] == 0:
# 			print('center')
# 			mobility.stop()
# 		if data['frameLocation'] == 2:
# 			print('right')
# 			mobility.moveRight()

# 		prevDir = data['frameLocation']
	
# 	mainLoop('furDetection')


sio.connect('http://192.168.1.21:3055')
sio.wait()
	