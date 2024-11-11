# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging
from datetime import datetime
import os
import subprocess
import csv
import joblib
import pandas as pd
from collections import Counter
import math
from io import BytesIO
import base64

# 로그 설정
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, datetime.today().strftime("%Y.%m.%d")+'.log'), level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

app.secret_key = os.urandom(64).hex()
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

output_dir = './outputs'
os.makedirs(output_dir, exist_ok=True)
output_csv_path = os.path.join(output_dir, 'outputs.csv')

# 엔트로피 계산 함수
def calculate_entropy(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    if not data:
        return 0.0
    counter = Counter(data)
    length = len(data)
    entropy = -sum((count / length) * math.log2(count / length) for count in counter.values())
    return entropy

# capa 분석 및 AI 예측 함수 (예시)
model_dir = './pca_models/model.pkl'
def model():
    model = joblib.load(model_dir)
    df = pd.read_csv(output_csv_path)
    df['Entropy'] = pd.to_numeric(df['Entropy'], errors='coerce')
    
    result_float = model.predict_proba(df)
    result_int = model.predict(df)
    return (result_float[0][0], result_float[0][1], result_int[0])

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        entropy = calculate_entropy(file_path)
        features = {
            'file_name': filename,
            'Entropy': entropy,
            'Example Field': 'Example Data'
        }

        with open(output_csv_path, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['file_name', 'Entropy', 'Example Field']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(features)

        a = model()
        normal_prob = float(a[0]) * 100
        virus_prob = float(a[1]) * 100

        os.remove(file_path)
        os.remove(output_csv_path)
            
        return jsonify({
            'normal_probability': a[0],
            'virus_probability': a[1],
            'classification': int(a[2])
        })
    except Exception as e:
        logging.error("An error occurred: " + str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
