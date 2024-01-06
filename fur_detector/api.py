import cv2 as cv
import os, uuid, base64
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
from coreFunc.detectorBot import TfLiteModel


app = Flask(__name__)
CORS(app)
api = Api(app)

image_path = 'imageUpload'
model = TfLiteModel(model='custom_model_lite/detect.tflite',
                                 label='custom_model_lite/labelmap.txt')


class detectorApi(Resource):
    def generateDetections(self,image):
        image = cv.imread(image)
        return model.detect_frame(image)
    
    def get(self):
        return jsonify({'data':'Recieved! from the server'})

    def post(self):
        data = request.get_json()

        dataBuffer = data['frameBuffer']
        image_type = base64.b64decode(dataBuffer)

        filename = secure_filename('sample.jpg')
        with open( 'imageUpload/'+ filename, 'wb') as output:
            output.write(image_type)

        detections = self.generateDetections(f'{image_path}/{filename}')
        if detections:
            return detections
        return {'error': 'No fur detected', 'status':404}

api.add_resource(detectorApi, '/furApi')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')