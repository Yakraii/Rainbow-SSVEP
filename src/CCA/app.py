from flask import Flask, request, jsonify
import subprocess
import json
import os
from module import getPath
# 读取路径
root_path = getPath.getRootPath()
py_path = os.path.join(root_path, 'src', 'CCA')

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the SSVEP Classification API. Use the /classify endpoint to classify data."

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    print(data)
    if data is None:
        return jsonify({
            "error": "No JSON data provided."
        }), 400

    file_name = data.get('file_name')
    if not file_name:
        return jsonify({"error": "file_name parameter is required"}), 400

    # 构建命令行参数
    cmd = [
        'python', os.path.join(py_path, 'FBCCA_SSVEP_Classification.py'),
        '--file_name', file_name
    ]

    try:
        # 启动子进程并获取输出
        result = subprocess.run(cmd, capture_output=True, text=True)

        # 检查子进程是否成功完成
        if result.returncode != 0:
            return jsonify({
                "error": "子进程失败。",
                "stderr": result.stderr
            }), 500

        # 解析输出
        output = result.stdout.strip()  # 去除多余的空格和换行符
        if not output:
            return jsonify({
                "error": "返回了空白的输出。"
            }), 500

        try:
            result_data = json.loads(output)
        except json.JSONDecodeError as e:
            return jsonify({
                "error": "无法将子进程的输出解析为JSON",
                "output": output,
                "exception": str(e)
            }), 500

        return jsonify(result_data)

    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "exception": str(e)
        }), 500

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    file_name = data.get('file_name')
    frequencies = data.get('frequencies', [])

    if not file_name:
        return jsonify({"error": "file_name parameter is required"}), 400

    # 构建命令行参数
    cmd = [
        'python', os.path.join(py_path, 'DataProcessing.py'),
        '--file_name', file_name
    ]

    if frequencies:
        cmd.extend(['--frequencies'] + [str(freq) for freq in frequencies])

    # 启动子进程并获取输出
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout

    # 解析输出
    try:
        result_data = json.loads(output)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse output from data processing script"}), 500

    return jsonify(result_data)


@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input (no data provide)"}), 400

    file_name = data.get('file_name')
    frequencies = data.get('frequencies', [])

    if not file_name:
        return jsonify({"error": "file_name parameter is required"}), 400

    # 构建命令行参数
    cmd = [
        'python', os.path.join(py_path, 'DataProcessing.py'),
        '--file_name', file_name
    ]

    if frequencies:
        cmd.extend(['--frequencies'] + [str(freq) for freq in frequencies])

    try:
        # 启动子进程并获取输出
        result = subprocess.run(cmd, capture_output=True, text=True)

        # 检查子进程是否成功完成
        if result.returncode != 0:
            return jsonify({
                "error": "子进程失败。",
                "stderr": result.stderr
            }), 500

        # 解析输出
        output = result.stdout.strip()  # 去除多余的空格和换行符
        if not output:
            return jsonify({
                "error": "返回了空白的输出。"
            }), 500

        return jsonify({"message": output})

    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "exception": str(e)
        }), 500
if __name__ == '__main__':
    app.run(debug=True)