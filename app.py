# app.py
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input

app = Flask(__name__)

MODEL_PATH = 'aksarajawa_cnn_model.h5'
model = load_model(MODEL_PATH)

uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

class_labels = ['ba', 'ca', 'da', 'dha', 'ga', 'ha', 'ja', 'ka', 'la', 'ma',
                'na', 'nga', 'nya', 'pa', 'ra', 'sa', 'ta', 'tha', 'wa', 'ya']

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(150, 150))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    predictions = model.predict(x)
    return predictions

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', prediction_result="")

@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(uploads_dir, secure_filename(file.filename))
            file.save(file_path)
            preds = model_predict(file_path, model)
            predicted_class_index = np.argmax(preds)
            predicted_class = class_labels[predicted_class_index]
            os.remove(file_path)
            return redirect(url_for('result', prediction_result=predicted_class))

    return render_template('index.html', prediction_result="No file uploaded.")

@app.route('/result/<prediction_result>')
def result(prediction_result):
    return render_template('result.html', prediction_result=prediction_result)

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
