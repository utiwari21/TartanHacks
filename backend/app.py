from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import cv2
import numpy as np
from deepface import DeepFace

app = Flask(__name__)
CORS(app)  # Allow React Native to connect

@app.route('/detect-emotion', methods=['POST'])
def detect_emotion():
    try:
        data = request.json
        image_data = data['image']  # Get Base64 image

        # Decode Base64 to OpenCV format
        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Analyze emotion
        analysis = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
        detected_emotion = analysis[0]['dominant_emotion']

        return jsonify({"emotion": detected_emotion})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
