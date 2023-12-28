import cv2 as cv
from detectorBot import TfLiteModel

class Vision:
    def __init__(self, resolution=(640,480), framerate=30):
        self.model = TfLiteModel(model='custom_model_lite/detect.tflite',
                                 label='custom_model_lite/labelmap.txt')
        self.camera = cv.VideoCapture(1)
        self.camera.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
        self.camera.set(3,resolution[0])
        self.camera.set(4,resolution[1])
        
        self.framerate = framerate
        self.prevTime = 0
        self.newTime = 0
        self.pixel = 32

    def getDirection(self,xAxis=0):
        return xAxis // self.pixel

    def getFrameRate(self):
        fps = 1/(self.newTime-self.prevTime) 
        self.prevTime = self.newTime 

        return fps

    def getDetection(self,frame):
        detection = self.model.detect_frame(frame)
        if detection:
            return self.getDirection(xAxis=
                                     detection[0][2])
        return  -1

    def captureFrame(self):
        success, frame = self.camera.read()
        return frame
    
    def displayFrame(self,frame,fps=None):
        cv.putText(frame,'FPS: {0:.2f}'.format(fps),(30,50),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv.LINE_AA)
        cv.imshow('fur detector', frame)

