import os
import time
from datetime import datetime
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams
import yaml
import sys
import argparse
from module import getPath


# 读取配置
root_path = getPath.getRootPath()
config_path = os.path.join(root_path, 'config', 'config.yaml')
with open(config_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)
    config_board = config['board']
    config_data = config['columns']

# 设置板参数
param = BrainFlowInputParams()
param.ip_address = config_board['ip_address']
param.ip_port = config_board['ip_port']
param.timeout = config_board['timeout']
board_id = config_board['board_id']

# 设置数据列
columns = config_data

# 创建板卡对象
board = BoardShim(board_id, param)


def init():
    try:
        board.prepare_session()
        if not board.is_prepared():
            print("板卡准备失败")
            sys.exit(1)
        print("BOARD_PREPARED_SUCCESS")  # 关键成功标识
        board.start_stream()
    except Exception as e:
        print(f"初始化错误: {str(e)}")
        sys.exit(1)


def mark():
    try:
        for marker in range(1, 6):
            board.insert_marker(marker)
            print(f"Insert {marker} begin")
            time.sleep(25)

            board.insert_marker(marker)
            print(f"Insert {marker} end")
            # if marker < 5:
            #     time.sleep(5)  # 最后一次不需要休息
    except AttributeError:
        pass


if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', required=True)
    args = parser.parse_args()

    # 使用传入的文件名
    data_path = os.path.join(root_path, 'data', 'data_raw', f"{args.file_name}.csv")

    try:
        init()
        time.sleep(1) # 等待前端开始闪烁
        # 自动执行标记插入流程
        mark()
        time.sleep(3) # 等待数据稳定
        # 数据保存
        data = board.get_board_data()
        df = pd.DataFrame(data.T, columns=columns)
        print("data_path: ", data_path)
        df.to_csv(data_path, index=False)
        print("Recording completed successfully")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        # 停止流并释放板卡
        board.stop_stream()
        board.release_all_sessions()

