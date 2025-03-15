import re
import time
from flask_cors import CORS
from flask import Flask, request, jsonify
import subprocess
import json
import os
from module import getPath
# 读取路径
root_path = getPath.getRootPath()
CCA_path = os.path.join(root_path, 'src', 'CCA')
dataporcess_path = os.path.join(root_path, 'src', 'getdata')

app = Flask(__name__)
CORS(app)  # 启用 CORS

@app.route('/')
def home():
    return "Welcome to the SSVEP Classification API. Use the /classify endpoint to classify data. Use the /process_data endpoint to process data. Use the /record_data endpoint to record data." 


@app.route('/classify', methods=['POST'])
def classify():
    """
    POST /classify
    这个接口用于启动 FBCCA_SSVEP_Classification.py 脚本，并传入 file_name 参数进行分类。

    请求体:
    {
        "file_name": "your_file_name_here"
    }

    响应:
    成功时返回分类结果的 JSON 数据。
    失败时返回错误信息。

    错误码:
    400 - 请求体中缺少必要的参数。
    500 - 子进程执行失败或输出解析失败。
    """
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
        'python', os.path.join(CCA_path, 'FBCCA_SSVEP_Classification.py'),
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

        # 提取以 RESULT: 开头的 JSON 数据
        output = result.stdout.strip()  # 去除多余的空格和换行符
        match = re.search(r"RESULT: (\{.*\})", output)  # 使用正则表达式提取 JSON 数据

        if not match:
            return jsonify({
                "error": "未找到有效的 JSON 数据。",
                "output": output
            }), 500

        try:
            result_data = json.loads(match.group(1))  # 解析提取的 JSON 数据
        except json.JSONDecodeError as e:
            return jsonify({
                "error": "无法将子进程的输出解析为JSON",
                "output": match.group(1),  # 打印提取的 JSON 数据
                "exception": str(e)
            }), 500

        # 返回结果，包括 average_scores
        return jsonify({
            "average_scores": result_data.get("average_scores"),
            "final_valid_acc_list": result_data.get("final_valid_acc_list")
        })

    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "exception": str(e)
        }), 500

@app.route('/process_data', methods=['POST'])
def process_data():
    """
    POST /process_data
    这个接口用于启动 DataProcessing.py 脚本，并传入 file_name 和 frequencies 参数进行数据处理。

    请求体:
    {
        "file_name": "7.5&10", #必选 不需要加.csv
        "frequencies": [7.5, 9.75, 10.25, 12.25, 14.25]  # 可选参数
    }

    响应:
    成功时返回数据处理结果的 JSON 数据。
    失败时返回错误信息。

    错误码:
    400 - 请求体中缺少必要的参数。
    500 - 子进程执行失败或输出解析失败。
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    file_name = data.get('file_name')
    frequencies = data.get('frequencies', [])

    if not file_name:
        return jsonify({"error": "file_name parameter is required"}), 400

    # 构建命令行参数
    cmd = [
        'python', os.path.join(dataporcess_path, 'DataProcessing.py'),
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

@app.route('/record_data', methods=['POST'])
def record_data():
    """
    POST /record_data
    这个接口用于启动 Marker_Recorder.py 脚本，传入 file_name 进行数据获取。

    请求体:
    {
        "file_name": "123 + 2025/3/15_11:29", #必选 文件名字
    }

    响应:
    板卡准备成功返回成功码，随后再开启闪烁（待写）。
    启动失败时返回错误信息。

    错误码:
    400 - 请求体中缺少必要的参数。
    500 - 子进程执行失败或输出解析失败。
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    file_name = data.get('file_name')
    if not file_name:
        return jsonify({"error": "file_name parameter is required"}), 400
    # 构建命令行参数
    cmd = [
        'python', os.path.join(dataporcess_path, 'Marker_Recorder.py'),
        '--file_name', file_name
    ]

    # 启动子进程并实时捕获输出
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        encoding='utf-8'
    )

    # 设置超时时间（单位：秒）
    timeout = 50 # 等待后端输出结果状态
    start_time = time.time()
    success = False

    while time.time() - start_time < timeout:
        # 非阻塞读取输出
        line = proc.stdout.readline()
        if "BOARD_PREPARED_SUCCESS" in line:
            success = True
            break
        if proc.poll() is not None:  # 子进程已退出
            break

    if success:
        # 返回成功，子进程继续在后台运行
        return jsonify({"message": "Recording started successfully (板卡准备成功！)"}), 200
    else:
        # 终止子进程并获取错误信息
        proc.terminate()
        stderr_output = proc.stderr.read()
        return jsonify({
            "error": "Failed to initialize board (板卡初始化失败)",
            "details": stderr_output.strip()
        }), 500

if __name__ == '__main__':
    app.run(debug=True)