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
    # data = request.get_json()

    # 构建命令行参数
    cmd = [
        'python', py_path + '/FBCCA_SSVEP_Classification.py'
    ]

    try:
        # 启动子进程并获取输出
        result = subprocess.run(cmd, capture_output=True, text=True)

        # 检查子进程是否成功完成
        if result.returncode != 0:
            return jsonify({
                "error": "Subprocess failed",
                "stderr": result.stderr
            }), 500

        # 解析输出
        output = result.stdout.strip()  # 去除多余的空格和换行符
        if not output:
            return jsonify({
                "error": "Subprocess returned empty output"
            }), 500

        try:
            result_data = json.loads(output)
        except json.JSONDecodeError as e:
            return jsonify({
                "error": "Failed to parse subprocess output as JSON",
                "output": output,
                "exception": str(e)
            }), 500

        return jsonify(result_data)

    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "exception": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)