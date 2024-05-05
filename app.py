from flask import Flask, render_template, request
import cv2
import numpy as np
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        # Read image file
        img_bytes = file.read()
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Resize the image
        new_width = int(request.form['width'])
        new_height = int(request.form['height'])
        resized_img = cv2.resize(img, (new_width, new_height))

        # Convert resized image to base64 for display
        retval, buffer = cv2.imencode('.jpg', resized_img)
        img_str = base64.b64encode(buffer).decode('utf-8')
        img_data = f'data:image/jpeg;base64,{img_str}'

        return render_template('index.html', img_data=img_data)

    return 'No file uploaded'

if __name__ == '__main__':
    app.run(debug=True)
