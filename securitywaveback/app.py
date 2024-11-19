from flask import Flask, request, jsonify
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
import matplotlib
matplotlib.use('Agg')  # GUI 백엔드 대신 'Agg' 백엔드를 사용하여 그래프 생성
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import platform
import traceback
from flask_cors import CORS
import sys

# matplotlib 로깅 레벨 설정 (DEBUG 메시지 무시)
matplotlib_logger = logging.getLogger('matplotlib')
matplotlib_logger.setLevel(logging.WARNING)  # DEBUG 대신 WARNING 이상의 메시지만 표시

# 프로젝트 루트 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 로깅 설정
log_dir = os.path.join(BASE_DIR, 'logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, datetime.today().strftime("%Y.%m.%d")+'.log'), level=logging.DEBUG)

app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "http://localhost:3000"}})
app.secret_key = os.urandom(64).hex()
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


#맥버전인 경우 'capa'로 수정 윈도우버전이라면 'capa.exe'로 수정 아마 이건 똑같을듯 << 이건 수정함
#capa_path = os.path.join(BASE_DIR, 'capa.exe')
# 운영 체제에 따라 capa 실행 파일 경로 설정
if platform.system() == 'Windows':
    capa_path = os.path.join(BASE_DIR, 'capa.exe')
else:
    capa_path = os.path.join(BASE_DIR, 'capa')

# 로깅으로 capa_path 확인
logging.info(f"Using capa path: {capa_path}")

output_csv_path = os.path.join(BASE_DIR, 'outputs', 'outputs.csv')
preprocess_path = os.path.join(BASE_DIR, 'preprocessing.py')

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

# capa 결과 파싱
def parse_capa_output(output):
    parsed_data = {
        'ATT&CK Tactic': [],
        'ATT&CK Technique': [],
        'MBC Objective': [],
        'MBC Behavior': [],
        'Namespace': [],
        'Capability': []
    }
    sections = output.split('\n\n')
    for idx, section in enumerate(sections):
        lines = section.strip().split('\n')
        if not lines:
            continue
        if idx != 0:
            parsed_data['Capability'].append(lines[0].strip())
        
        for line in lines[1:] if idx != 0 else lines:
            if 'namespace' in line:
                match = re.search(r'namespace\s+(\S+)', line)
                if match:
                    parsed_data['Namespace'].append(match.group(1).strip())
            if 'mbc' in line:
                match = re.search(r'mbc\s+([^\:]+)\s*\:\s*([^,\n]+)', line, re.IGNORECASE)
                if match:
                    parsed_data['MBC Objective'].append(match.group(1).strip())
                    parsed_data['MBC Behavior'].append(match.group(2).strip())
            if 'att&ck' in line:
                match = re.search(r'att&ck\s+([^\:]+)\s*\:\s*([^,\n]+)', line, re.IGNORECASE)
                if match:
                    parsed_data['ATT&CK Tactic'].append(match.group(1).strip())
                    parsed_data['ATT&CK Technique'].append(match.group(2).strip())

    for key in parsed_data:
        parsed_data[key] = '; '.join(set(parsed_data[key]))

    return parsed_data

# capa 실행 함수
def capa(file_path):
    try:
        start_time = datetime.now()
        result = subprocess.run([capa_path, '-vv', file_path], capture_output=True, text=True, encoding='utf-8')
        end_time = datetime.now()
        logging.info(f"Time taken for capa analysis: {end_time - start_time}")

        if result.stdout:
            parsed_data = parse_capa_output(result.stdout)
            parsed_data['file_name'] = os.path.basename(file_path)
            parsed_data['Entropy'] = calculate_entropy(file_path)
            return parsed_data
        else:
            return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running capa: {str(e)}")
        return None

# AI 모델 예측 함수
model_dir = os.path.join(BASE_DIR, 'pca_models', 'model.pkl')
def model():
    model = joblib.load(f"{model_dir}")

    # 전처리 시간 측정
    preprocess_start = datetime.now()
    subprocess.run([sys.executable, preprocess_path])
    preprocess_end = datetime.now()
    logging.info(f"Time taken for preprocessing: {preprocess_end - preprocess_start}")

    # 전처리 후 데이터 프레임 로드
    df = pd.read_csv(output_csv_path)

    # 전처리된 CSV 파일과 모델 특성 개수가 일치하는지 확인
    if df.shape[1] != model.n_features_in_:
        logging.error("CSV file format does not match model features.")
        raise ValueError(f"CSV file has {df.shape[1]} columns, but model requires {model.n_features_in_} columns.")
    
    df['Entropy'] = pd.to_numeric(df['Entropy'], errors='coerce')

    # 모델 예측 시간 측정
    predict_start = datetime.now()
    result_float = model.predict_proba(df).flatten()
    result_int = model.predict(df)[0]
    predict_end = datetime.now()
    logging.info(f"Time taken for AI model prediction: {predict_end - predict_start}")

    return result_float[0], result_float[1], result_int

# 그래프 생성 함수
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

# 보안 헤더 추가
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # outputs.csv 및 mitre/outputs.csv 초기화
        open(output_csv_path, 'w').close()
        mitre_csv_path = os.path.join(BASE_DIR, 'mitre', 'outputs.csv')
        os.makedirs(os.path.dirname(mitre_csv_path), exist_ok=True)
        open(mitre_csv_path, 'w').close()

        # 파일 업로드 확인
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # 파일 저장
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # capa 분석 수행
        features = capa(file_path)
        if features is None:
            return jsonify({'error': 'Capa analysis failed'}), 500

        # CSV에 데이터 쓰기
        fieldnames = ['file_name', 'Entropy', 'ATT&CK Tactic', 'ATT&CK Technique', 'MBC Objective', 'MBC Behavior', 'Namespace', 'Capability']

        # outputs.csv에 저장
        with open(output_csv_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(features)

        # mitre/outputs.csv에 저장
        with open(mitre_csv_path, 'a', newline='', encoding='utf-8') as mitre_file:
            writer = csv.DictWriter(mitre_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(features)

        # CSV에서 두 번째 행의 네 번째 열 가져오기
        second_row_fourth_column = None
        with open(mitre_csv_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)

            # 데이터 확인 및 가져오기
            if len(rows) > 1 and len(rows[1]) > 3:
                second_row_fourth_column = rows[1][3]
        
        # 로그 기록
        app.logger.debug(f"Second row, fourth column (ATT&CK Technique): {second_row_fourth_column}")

        # 모델 예측 및 차트 생성
        result_probs = model()
        chart_data = create_pie_chart(result_probs[0] * 100, result_probs[1] * 100)

        # 업로드한 파일 삭제
        os.remove(file_path)

        # 응답 데이터
        return jsonify({
            'classification': int(float(result_probs[2])),
            'chart_data': chart_data,
            'second_row_fourth_column': second_row_fourth_column
        })
    except Exception as e:
        logging.error("An error occurred during file upload: " + str(e))
        logging.error(traceback.format_exc())
        return jsonify({'error': 'An internal server error occurred'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
