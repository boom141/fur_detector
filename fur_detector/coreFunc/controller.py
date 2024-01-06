from gpiozero import Robot
from time import sleep

class Mobility:
	defaultDelay = 1
	def __init__(self):
		self.vaccum = Robot(left=(23, 22), right=(17, 18))
		self.mode = 'automatic'

	def moveForward(self,delay=defaultDelay):
		self.vaccum.forward()
		sleep(delay)

	def moveBackward(self,delay=defaultDelay):
		self.vaccum.backward()
		sleep(delay)

	def moveRight(self,delay=defaultDelay):
		self.vaccum.right()
		sleep(delay)
  
	def moveLeft(self,delay=defaultDelay):
		print(delay)
		self.vaccum.left()
		sleep(delay)

	def stop(self):
		self.vaccum.stop()

	def runCalibrate(self):
		self.moveForward()
		self.moveBackward()
		self.moveLeft()
		self.moveRight()
		self.moveLeft()

	def runRandomPath(self):
		pass

