import os
import subprocess
import csv
import re
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter

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
            current_capability = lines[0].strip()
            parsed_data['Capability'].append(current_capability)
        
        for line in lines[1:] if idx != 0 else lines:  
            if 'namespace' in line:
                namespace_match = re.search(r'namespace\s+(\S+)', line)
                if namespace_match:
                    parsed_data['Namespace'].append(namespace_match.group(1).strip())

            if 'mbc' in line:
                mbc_match = re.search(r'mbc\s+([^\:]+)\s*\:\s*([^,\n]+)', line, re.IGNORECASE)
                if mbc_match:
                    parsed_data['MBC Objective'].append(mbc_match.group(1).strip())
                    parsed_data['MBC Behavior'].append(mbc_match.group(2).strip())

            if 'att&ck' in line:
                attack_match = re.search(r'att&ck\s+([^\:]+)\s*\:\s*([^,\n]+)', line, re.IGNORECASE)
                if attack_match:
                    parsed_data['ATT&CK Tactic'].append(attack_match.group(1).strip())
                    parsed_data['ATT&CK Technique'].append(attack_match.group(2).strip())

    for key in parsed_data:
        parsed_data[key] = '; '.join(set(parsed_data[key]))

    return parsed_data

def calculate_entropy(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    if not data:
        return 0.0
    counter = Counter(data)
    length = len(data)
    entropy = -sum((count / length) * math.log2(count / length) for count in counter.values())
    return entropy

def process_file(capa_path, file_path):
    try:
        print('Capa : ',file_path)
        result = subprocess.run([capa_path, '-vv', file_path], capture_output=True, text=True, shell=True, encoding='utf-8')
        if result.stdout:
            parsed_data = parse_capa_output(result.stdout)
            parsed_data['file_name'] = os.path.basename(file_path)
            parsed_data['Entropy'] = calculate_entropy(file_path)
            return parsed_data
        else:
            print(f"No output from capa for file: {file_path}")
            print("stderr:", result.stderr)  # 추가하여 stderr 출력

    except subprocess.CalledProcessError as e:
        print(f"Capa failed to run on {file_path}: {str(e)}")
    return None

def run_capa_and_save_to_csv(input_directory, output_csv_path, max_workers):
    capa_path = r'/Users/skgus/Downloads/IRmeetup/capa' #cmd 창에 프로그램입력 (capa.exe 경로)
    
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['file_name', 'Entropy', 'ATT&CK Tactic', 'ATT&CK Technique', 'MBC Objective', 'MBC Behavior', 'Namespace', 'Capability']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        file_paths = [os.path.join(root, filename) for root, dirs, files in os.walk(input_directory) for filename in files]

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_file, capa_path, file_path): file_path for file_path in file_paths}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    writer.writerow(result)
    print('Done')
input_directory = './test' # 탐색할 폴더 위치
output_csv_path = './outputs/output.csv' # 저장할 CSV 파일 명
print('Starting')
run_capa_and_save_to_csv(input_directory, output_csv_path, 5)
