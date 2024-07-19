# ola

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
import cv2
import numpy as np
import io
from PIL import Image

app = Flask(__name__, static_folder='static')
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@socketio.on('message')
def handle_message(data):
    image_bytes = io.BytesIO(data)
    image = Image.open(image_bytes)
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(processed_image_rgb)
    
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
    socketio.send(buffered.getvalue())  # Change from emit to send for simplicity

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
