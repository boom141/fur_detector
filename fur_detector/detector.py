import cv2 as cv
from fur_detector_bot import TfLiteModel

class CameraDetector:

    @classmethod    
    def start(cls):
        camera = cv.VideoCapture(0)

        while 1:
            success, frame = camera.read()

            if not success:
                break
            
            # image_buffer = cv.imencode('.jpg', frame)[1]
            # image_data = base64.b64encode(image_buffer)
  
            TfLiteModel.detect_frame(frame)
            cv.imshow('fur detector', frame)
            
            if cv.waitKey(1) == ord('q'):
                break

        camera.release()
        cv.destroyAllWindows()


