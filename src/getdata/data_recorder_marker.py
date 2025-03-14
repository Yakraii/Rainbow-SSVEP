import os
import time
from datetime import datetime
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations, WindowOperations, AggOperations
from pynput import keyboard
import yaml
from matplotlib import pyplot as plt
from pprint import pprint
from module import getPath

# 读取配置
root_path = getPath.getRootPath()
config_path = os.path.join(root_path, 'config', 'config.yaml')
with open(config_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)
    config_board = config['board']
    config_data = config['columns']
# pprint(config)


# 生成带有时间戳的文件名
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
data_path = os.path.join(root_path, 'data', f"data_{current_time}.csv")
print("data_path: ",data_path)

# 设置板参数
param = BrainFlowInputParams()
param.sample_rate = 256
param.ip_address = config_board['ip_address']
param.ip_port = config_board['ip_port']
param.timeout = config_board['timeout']
board_id = config_board['board_id']
duration = config_board['duration']

# 设置数据列
columns = config_data

# 创建板卡对象
board = BoardShim(board_id, param)


def init():
    board.prepare_session()  # 准备板卡
    if board.is_prepared():
        print('板卡已准备')
    board.start_stream()  # 开始数据流

def on_press(key):
    try:
        # 创建键盘键与标记的映射字典
        keydict = {
            keyboard.Key.enter: (1, 'Pressed: enter  插入标记 66666'),
            keyboard.Key.f1: (666, 'Pressed: F1  插入标记 A(1)'),
            keyboard.Key.f2: (2, 'Pressed: F2  插入标记 B(2)'),
            keyboard.Key.f3: (3, 'Pressed: F3  插入标记 C(3)'),
            keyboard.Key.f4: (4, 'Pressed: F4  插入标记 D(4)'),
            keyboard.Key.f5: (5, 'Pressed: F5  插入标记 E(5)'),
            keyboard.Key.f6: (6, 'Pressed: F6  插入标记 F(6)'),
            keyboard.Key.f7: (7, 'Pressed: F7  插入标记 G(7)'),
            keyboard.Key.f8: (8, 'Pressed: F8  插入标记 H(8)'),
            keyboard.Key.f9: (9, 'Pressed: F9  插入标记 I(9)'),
            keyboard.Key.f10: (10, 'Pressed: F10  插入标记 J(10)'),
            keyboard.Key.f11: (11, 'Pressed: F11  插入标记 K(11)'),
            keyboard.Key.f12: (12, 'Pressed: F12  插入标记 L(12)'),
        }

        # 打标
        if key in keydict:
            marker, message = keydict[key]
            print(message)
            board.insert_marker(marker)

    except AttributeError:
        pass

def draw():
    count = 0
    fig, axs = plt.subplots(8, 1, figsize=(10, 12), sharex=True)  # 创建8个子图
    for ax in axs:
        ax.set_ylim(-500, 500)
        ax.axis('off')

    flag=time.time()
    start_time = time.time()
    # 持续时间内画图
    while time.time() - start_time < duration:
        if(time.time()-flag>=1):
            # print(time.time() - flag, " 更新绘图")
            for ax in axs:
                ax.cla()  # 清除之前的绘图

            # 获取实时数据  
            current_data = board.get_current_board_data(1000)
            # 打印数据
            print(current_data) 
            channels = board.get_eeg_channels(board_id)
            for i, channel in enumerate(channels):
                data_x = [j for j in range(len(current_data[channel]))]
                print("data_x: ",data_x)
                data_y = current_data[channel]
                # 数据预处理：去趋势和滤波
                DataFilter.detrend(data_y, DetrendOperations.CONSTANT.value)  # 去趋势
                DataFilter.perform_bandpass(data_y, 1000, 3.0, 45.0, 4, FilterTypes.BUTTERWORTH.value, 0)  # 带通滤波
                DataFilter.perform_bandstop(data_y, 1000, 48.0, 52.0, 2, FilterTypes.BUTTERWORTH.value, 0)  # 带阻滤波（50Hz工频）
                DataFilter.perform_bandstop(data_y, 1000, 58.0, 62.0, 2, FilterTypes.BUTTERWORTH.value, 0)  # 带阻滤波（60Hz工频）
                axs[i].plot(data_x, data_y)  # 绘制每个通道的数据
            plt.draw() # 绘制图形
            plt.pause(0.05)  # 更新图形
            flag=time.time()

def main():
    # 获取板卡描述信息
    # board_describe = BoardShim.get_board_descr(board_id)
    # print('板卡描述信息：')
    # pprint(board_describe)
    # 创建键盘监听器，在按下键时调用 on_press
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # 在后台启动监听器
    draw()
    try:
        # 保存到文件
        data = board.get_board_data()
        df = pd.DataFrame(data.T, columns=columns)
        df.to_csv(data_path, index=False)

    finally:
        # 停止数据流并释放资源
        board.stop_stream()
        board.release_all_sessions()
        listener.stop()


if __name__ == '__main__':
    init()
    main()
