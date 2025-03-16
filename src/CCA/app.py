import re
import threading
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
app.debug = True
CORS(app)  # 启用 CORS

def wait_for_success(proc, timeout):
    """
    等待子进程输出 BOARD_PREPARED_SUCCESS，超时则返回 False。
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        # 检查子进程是否已退出
        if proc.poll() is not None:
            return False
        # 读取一行输出
        line = proc.stdout.readline()
        if line:
            print(f"[子进程输出] {line.strip()}")
            if "BOARD_PREPARED_SUCCESS" in line:
                return True
        time.sleep(0.1)  # 避免 CPU 占用过高
    return False

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
        'python', '-u', os.path.join(CCA_path, 'FBCCA_SSVEP_Classification.py'),
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
        'python', '-u', os.path.join(dataporcess_path, 'DataProcessing.py'),
        '--file_name', file_name
    ]

    if frequencies:
        cmd.extend(['--frequencies'] + [str(freq) for freq in frequencies])

    # 启动子进程并实时捕获输出
    result = subprocess.run(cmd, capture_output=True, text=True)

    # 检查子进程是否成功完成
    if result.returncode != 0:
        return jsonify({
            "error": "子进程失败。",
            "stderr": result.stderr
        }), 500

    # 提取以 Save Successfully 开头的数据
    output = result.stdout.strip()  # 去除多余的空格和换行符
    match = re.search(r"Save Successfully:\s+(\S+)", output)

    if match:
        saved_file_path = match.group(1)  # 提取保存的文件路径
        return jsonify({
            "message": "Data processing completed (数据处理完毕)",
            "saved_file_path": saved_file_path
        }), 200
    else:
        return jsonify({
            "error": "Save failed (保存失败)",
            "details": output  # 返回完整的子进程输出以便调试
        }), 500
    

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

    cmd = [
        'python', '-u', os.path.join(dataporcess_path, 'Marker_Recorder.py'),
        '--file_name', file_name
    ]

    # 启动子进程
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding='utf-8',
        errors='replace',
    )

    # 等待子进程输出 BOARD_PREPARED_SUCCESS
    timeout = 10  # 超时时间（秒）
    success = wait_for_success(proc, timeout)

    if success:
        # 启动后台线程继续捕获输出
        def background_reader(p):
            with p.stdout:
                for line in iter(p.stdout.readline, ''):
                    print(f"[子进程后续输出] {line.strip()}")
            p.wait()  # 等待子进程完全结束

        # 启动后台线程继续捕获输出
        threading.Thread(
            target=background_reader,  # 后台线程的目标函数
            args=(proc,),  # 传递给目标函数的参数
            daemon=True  # 将线程设置为守护线程
        ).start()

        return jsonify({"message": "Recording started successfully (板卡准备成功！)"}), 200
    else:
        # 超时或子进程异常退出
        proc.terminate()
        remaining_output = proc.stdout.read()
        return jsonify({
            "error": "板卡准备超时或子进程异常退出",
            "details": remaining_output.strip()
        }), 500

if __name__ == '__main__':
    app.run(debug=True)