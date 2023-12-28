from gpiozero import Robot
from time import sleep

class Mobility:
	def __init__(self):
		self.vaccum = Robot(left=(23, 22), right=(17, 18))
		self.mode = 'automatic'

	def moveForward(self,delay=2):
		self.vaccum.forward()
		sleep(delay)

	def moveBackward(self,delay=2):
		self.vaccum.backward()
		sleep(delay)

	def moveRight(self,delay=2):
		self.vaccum.right()
		sleep(delay)
  
	def moveLeft(self,delay=2):
		self.vaccum.left()
		sleep(delay)


	def runCalibrate(self):
		self.moveForward()
		self.moveBackward()
		self.moveLeft()
		self.moveRight(delay=4)
		self.moveLeft()

	def focusedObject(self,location):
		if location <= 3:
			self.moveLeft()
			print('moving left')
		elif location >= 12:
			self.moveRight()
			print('moving right')

	def runRandomPath(self):
		pass

