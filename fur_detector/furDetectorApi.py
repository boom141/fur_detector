import cv2 as cv
import numpy as np
import base64, io
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from detectorBot import TfLiteModel

app = Flask(__name__)
CORS(app)
api = Api(app)


class detectorApi(Resource):
    def post(self):
        image_file = request.get_data()
        binary = base64.b64decode(image_file)
        ImageByteArray = io.BytesIO(binary)
        print(ImageByteArray)

        # print(TfLiteModel.detect_frame(ImageByteArray))


api.add_resource(detectorApi, '/detectFur')

if __name__ == '__main__':
    app.run(debug=True)