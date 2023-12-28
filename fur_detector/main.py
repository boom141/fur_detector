import time
import cv2 as cv
# from controller import Mobility
from streaming import Vision

def mainLoop():
	#mobility = Mobility()
	vision = Vision()

	#mobility.runCalibrate()

	while vision.camera.isOpened():
		vision.newTime = time.time()

		frame = vision.captureFrame()
		objectLocation = vision.getDetection(frame)
		
		if objectLocation > 3 and objectLocation < 12:
			print("center")
		else:
			mobility.focusedObject(objectLocation)

		fps = vision.getFrameRate()
		vision.displayFrame(frame,fps=fps)

		if cv.waitKey(1) & 0xFF == ord('q'): 
			break

	vision.camera.release()
	cv.destroyAllWindows() 

mainLoop()
	
# sio = socketio.Client()

# @sio.event
# def connect():
#     sio.emit('authenticate_device', data=create_config())


# sio.connect('http://localhost:5000')
# sio.wait()
