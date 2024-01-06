import base64
import cv2 as cv

class Vision:
    def __init__(self, resolution=(640,480), framerate=30):
        self.camera = cv.VideoCapture(0)
        self.camera.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
        self.resolution = resolution
        self.camera.set(3,self.resolution[0])
        self.camera.set(4,self.resolution[1])

        self.framerate = framerate
        self.prevTime = 0
        self.newTime = 0

    def getFrameBytes(self):
        imageBuffer = cv.imencode('.jpg', self.frame)[1]
        b64Buffer = base64.b64encode(imageBuffer)
        
        return b64Buffer

    def captureFrame(self):        
        return self.camera.read()

    def getFrameRate(self):
        fps = 1/(self.newTime-self.prevTime) 
        self.prevTime = self.newTime 

        return fps

    def displayFrame(self,frame,fps=None):
        cv.putText(frame,'FPS: {0:.2f}'.format(fps),(30,50),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv.LINE_AA)
        cv.imshow('fur detector', frame)

