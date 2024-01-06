import cv2
import numpy as np
import importlib.util

class TfLiteModel:
    
    def __init__(self,model,label):
        self.model = model
        self.label = label
        self.filterName = ['White', 'Black', 'Gray', 'Beige']
        self.margin = (295,345)

        liteIntepreter = importlib.util.find_spec('tflite_runtime')
        if liteIntepreter:
            from tflite_runtime.interpreter import Interpreter
            print('[SUCCESS] Using tflite-runtime interpreter')
        else:
            from tensorflow.lite.python.interpreter import Interpreter
            print('[SUCCESS] Using tensorflow interpreter')

        self.tfInterpreter = Interpreter

    def detect_frame(self,img_data,min_conf=0.5):

        # Load the label map into memory
        with open(self.label, 'r') as f:
            labels = [line.strip() for line in f.readlines()]

        # Load the Tensorflow Lite model into memory
        interpreter = self.tfInterpreter(model_path=self.model)
        interpreter.allocate_tensors()

        # Get model details
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        height = input_details[0]['shape'][1]
        width = input_details[0]['shape'][2]

        float_input = (input_details[0]['dtype'] == np.float32)

        input_mean = 127.5
        input_std = 127.5

        # Load image and resize to expected shape [1xHxWx3]
        image = img_data
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imH, imW, _ = image.shape
        image_resized = cv2.resize(image_rgb, (width, height))
        input_data = np.expand_dims(image_resized, axis=0)

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if float_input:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'],input_data)
        interpreter.invoke()

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[1]['index'])[0] # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[3]['index'])[0] # Class index of detected objects
        scores = interpreter.get_tensor(output_details[0]['index'])[0] # Confidence of detected objects

        if ((scores[0] > min_conf) and (scores[0] <= 1.0)):
            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(boxes[0][0] * imH)))
            xmin = int(max(1,(boxes[0][1] * imW)))
            ymax = int(min(imH,(boxes[0][2] * imH)))
            xmax = int(min(imW,(boxes[0][3] * imW)))
            center = (int((xmin+xmax) // 2), int((ymin+ymax)//2))


            # Draw label
            object_name = labels[int(classes[0])] # Look up object name from "labels" array using class index
            if object_name not in self.filterName:
                # cv2.rectangle(image, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
                # label = '%s: %d%%' % (object_name, int(scores[0]*100)) # Example: 'person: 72%'
                # labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 5) # Get font size
                # label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                # cv2.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                # cv2.putText(image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
                # cv2.circle(image, center, 10, (0,0,255), -1)

                perspectiveLocation = 0
                if center[0] <= self.margin[0]:
                    perspectiveLocation = 1
                elif center[0] >= self.margin[1]:
                    perspectiveLocation = 2
                elif (center[0] > self.margin[0] 
                    and center[0] < self.margin[1]):
                    perspectiveLocation = 0

                return {'name':object_name, 'frameLocation':perspectiveLocation, 
                        'border':[ymin,ymax,xmin,xmax,center], 'frameMargin':self.margin,
                        'status':200}
            
        return {'message':'No detection found', 'status':404}
        

