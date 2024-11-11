# app.py
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging
from datetime import datetime
import os
import subprocess
import csv
import re
import math
from collections import Counter
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# 로그 설정
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, datetime.today().strftime("%Y.%m.%d")+'.log'), level=logging.DEBUG)

# React 빌드 파일 위치 지정
app = Flask(__name__, static_folder='../securityWaveFront/build/static', template_folder='../securityWaveFront/build')
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

# capa 분석 함수 (예시)
def capa(file_path):
    try:
        result = subprocess.run(['capa', '-vv', file_path], capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            parsed_data = {
                'file_name': os.path.basename(file_path),
                'Entropy': calculate_entropy(file_path),
                'Example Field': 'Example Data'
            }
            return parsed_data
        else:
            return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running capa: {str(e)}")
        return None

# 머신러닝 모델 예측 함수
model_dir = './pca_models/model.pkl'
def model():
    model = joblib.load(model_dir)
    df = pd.read_csv(output_csv_path)
    df['Entropy'] = pd.to_numeric(df['Entropy'], errors='coerce')
    
    result_float = model.predict_proba(df)
    result_int = model.predict(df)
    return (result_float[0][0], result_float[0][1], result_int[0])

# 차트 생성 함수
def create_pie_chart(normal_prob, virus_prob):
    labels = ['Normal', 'Malicious']
    sizes = [normal_prob, virus_prob]
    colors = ['#4CAF50', '#FF5733']
    explode = (0, 0.1)

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)
    return chart_data

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

        # capa 분석 수행
        features = capa(file_path)
        if features is None:
            return jsonify({'error': 'Capa analysis failed'}), 500

        # CSV에 데이터 쓰기
        with open(output_csv_path, 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['file_name', 'Entropy', 'Example Field']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(features)

        a = model()
        normal_prob = float(a[0]) * 100
        virus_prob = float(a[1]) * 100
        chart_data = create_pie_chart(normal_prob, virus_prob)
        
        os.remove(file_path)
        os.remove(output_csv_path)
            
        return jsonify({
            'normal_probability': a[0],
            'virus_probability': a[1],
            'classification': int(a[2]),
            'chart_data': chart_data
        })
    except Exception as e:
        logging.error("An error occurred: " + str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500

# React 애플리케이션의 index.html 제공
@app.route('/')
def serve_react_app():
    return render_template('index.html')

# 정적 파일 제공 (React의 정적 파일에 대한 경로 설정)
@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
