import os
import time
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations, WindowOperations, AggOperations
from matplotlib import pyplot as plt
import keyboard
import yaml

from pprint import pprint
from src.module import getPath

# 两个版本的main函数
# 第一个是实时波形图为原始EEG（最后统一滤波处理，减少重复计算，提高性能）
# 第二个是实时波形图为实时波形图为经过滤波、去趋势后的EEG（可以根据图来看处理的怎么样（？））


# 读取配置
root_path = getPath.getRootPath()
config_path = os.path.join(root_path, 'config', 'config.yaml')
with open(config_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)['board']
pprint(config)

# 设置参数
param = BrainFlowInputParams()
param.ip_address = config['ip_address']
param.ip_port = config['ip_port']
param.timeout = config['timeout']
board_id = config['board_id']
count_MAX = config['count_MAX']

board = BoardShim(board_id, param)

def init():
    # 准备板卡
    board.prepare_session()
    if board.is_prepared():
        print('板卡已准备')
    # 开始数据流
    board.start_stream()

def main1(): # 实时波形图为原始EEG
    # 实时绘制
    count = 0
    fig, axs = plt.subplots(8, 1, figsize=(10, 12), sharex=True)  # 创建8个子图
    for ax in axs:
        ax.set_ylim(-500, 500)
        ax.axis('off')

    # 标记和截取数据的设置
    markers = []

    while count < count_MAX:
        # 清除之前的绘图
        # for ax in axs:
        #     ax.cla()

        # 获取实时数据
        current_data = board.get_current_board_data(100)
        print(board.get_eeg_channels(board_id))

        # 获取通道数据并绘制（原始EEG）
        channels = board.get_eeg_channels(board_id)
        # for i, channel in enumerate(channels):
        #     data_x = [j for j in range(len(current_data[channel]))]
        #     data_y = current_data[channel]
        #     axs[i].plot(data_x, data_y)  # 绘制每个通道的数据
        #
        # plt.draw()
        # plt.pause(0.05)

        # 每隔10次插入标记
        if count % 10 == 0:  # 每隔10次插入一次标记，约每秒一次
            for key in 'abcdefghijklmnopqrstuvwxyz':  # 监测字母a-z
                if keyboard.is_pressed(key):
                    print(f'准备开始注视字母 {key.upper()}...')
                    time.sleep(5)  # 计时5秒
                    print(f'5秒结束，开始记录标记 {key.upper()}')
                    marker_time = count  # 记录插入标记的时间点
                    board.insert_marker(ord(key) - ord('a') + 1)  # 将字母转换为数字标记，例如，A->1, B->2
                    markers.append((marker_time, key.upper()))  # 保存标记和时间
                    break  # 一次只记录一个标记

        count += 1

    # 获取完整的板卡数据
    data = board.get_board_data()

    # 统一处理滤波，去趋势
    channels = board.get_eeg_channels(board_id)
    sampling_rate = board.get_sampling_rate(board_id)

    for channel in channels:
        # 去趋势
        DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
        # 带通滤波
        DataFilter.perform_bandpass(data[channel], sampling_rate, 3.0, 45.0, 4, FilterTypes.BUTTERWORTH.value, 0)
        # 带阻滤波
        DataFilter.perform_bandstop(data[channel], sampling_rate, 48.0, 52.0, 2, FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandstop(data[channel], sampling_rate, 58.0, 62.0, 2, FilterTypes.BUTTERWORTH.value, 0)

    # 将标记信息添加到数据
    data_with_markers = []

    for i in range(data.shape[1]):  # 遍历所有数据点
        row = data[:, i].tolist()
        # 默认没有标记
        marker = ''
        for marker_time, char in markers:
            if marker_time == i:
                marker = char
                break
        row.append(marker)  # 添加标记到行末
        data_with_markers.append(row)

    # 保存数据到文件
    df = pd.DataFrame(data_with_markers, columns=[f'Channel_{i + 1}' for i in range(data.shape[0])] + ['Markers'])
    df.to_csv('./marker.csv', index=False)
    print(f'数据形状: {data.shape}')

    # 获取标记通道数据
    marker_channel = board.get_marker_channel(board_id)
    labels = data[marker_channel]

    # 打印标记和截取的子数据 计算功率谱
    psd_size = DataFilter.get_nearest_power_of_two(sampling_rate)
    for index in range(len(labels)):
        label = labels[index]
        if label != 0:
            print(f'标记：{label}, 索引：{index}')
            sub_data = data[:, index:index + 700]  # 截取从标记位置开始的700个数据点
            print(f'截取的数据形状：{sub_data.shape}')
            for channel in channels:
                # 对数据进行下采样
                downsampled_data = DataFilter.perform_downsampling(data[channel], 2, AggOperations.MEDIAN)
                # 计算功率谱
                pxx, frequency = DataFilter.get_psd_welch(downsampled_data, psd_size, psd_size // 2,
                                                          sampling_rate, WindowOperations.BLACKMAN_HARRIS.value)
                print(f'通道 {channel} 的功率谱计算完成')

    # 结束接收
    board.stop_stream()
    board.release_all_sessions()

def main2(): # 实时波形图为经过滤波、去趋势后的EEG
    # 连接openbci 初始化参数
    param = BrainFlowInputParams()
    param.ip_address = "192.168.31.41"
    param.ip_port = 9527
    param.timeout = 1000
    board_id = 532  # 5/16/532/564
    board = BoardShim(board_id, param)

    # 准备板卡
    board.prepare_session()
    if board.is_prepared():
        print('板卡已准备')

    # 开始数据流
    board.start_stream()

    # 实时绘制
    count = 0
    fig, axs = plt.subplots(8, 1, figsize=(10, 12), sharex=True)  # 创建8个子图
    for ax in axs:
        ax.set_ylim(-500, 500)
        ax.axis('off')

    # 标记和截取数据的设置
    markers = []

    while count < count_MAX:
        # 清除之前的绘图
        for ax in axs:
            ax.cla()

        # 获取实时数据
        current_data = board.get_current_board_data(5000)

        # 获取通道数据并绘制（处理后的EEG）
        channels = board.get_eeg_channels(board_id)
        for i, channel in enumerate(channels):
            data_x = [j for j in range(len(current_data[channel]))]
            data_y = current_data[channel]
            # 数据预处理：去趋势和滤波
            DataFilter.detrend(data_y, DetrendOperations.CONSTANT.value)  # 去趋势
            DataFilter.perform_bandpass(data_y, 1000, 3.0, 45.0, 4, FilterTypes.BUTTERWORTH.value, 0)  # 带通滤波
            DataFilter.perform_bandstop(data_y, 1000, 48.0, 52.0, 2, FilterTypes.BUTTERWORTH.value, 0)  # 带阻滤波（50Hz工频）
            DataFilter.perform_bandstop(data_y, 1000, 58.0, 62.0, 2, FilterTypes.BUTTERWORTH.value, 0)  # 带阻滤波（60Hz工频）
            axs[i].plot(data_x, data_y)  # 绘制每个通道的数据

        plt.draw()
        plt.pause(0.05)

        # 每隔10次插入标记
        if count % 10 == 0:  # 每隔10次插入一次标记，约每秒一次
            for key in 'abcdefghijklmnopqrstuvwxyz':  # 监测字母a-z
                if keyboard.is_pressed(key):
                    print(f'准备开始注视字母 {key.upper()}...')
                    time.sleep(5)  # 计时5秒
                    print(f'5秒结束，开始记录标记 {key.upper()}')
                    marker_time = count  # 记录插入标记的时间点
                    board.insert_marker(ord(key) - ord('a') + 1)  # 将字母转换为数字标记，例如，A->1, B->2
                    markers.append((marker_time, key.upper()))  # 保存标记和时间
                    break  # 一次只记录一个标记

        count += 1

    # 获取完整的板卡数据
    data = board.get_board_data()

    # 将标记信息添加到数据
    data_with_markers = []

    for i in range(data.shape[1]):  # 遍历所有数据点
        row = data[:, i].tolist()
        # 默认没有标记
        marker = ''
        for marker_time, char in markers:
            if marker_time == i:
                marker = char
                break
        row.append(marker)  # 添加标记到行末
        data_with_markers.append(row)

    # 保存数据到文件
    df = pd.DataFrame(data_with_markers, columns=[f'Channel_{i + 1}' for i in range(data.shape[0])] + ['Markers'])
    df.to_csv('./marker.csv', index=False)
    print(f'数据形状: {data.shape}')

    # 获取标记通道数据
    marker_channel = board.get_marker_channel(board_id)
    labels = data[marker_channel]
    channels = board.get_eeg_channels(board_id)
    sampling_rate = board.get_sampling_rate(board_id)

    # 打印标记和截取的子数据 计算功率谱
    psd_size = DataFilter.get_nearest_power_of_two(sampling_rate)
    for index in range(len(labels)):
        label = labels[index]
        if label != 0:
            print(f'标记：{label}, 索引：{index}')
            sub_data = data[:, index:index + 700]  # 截取从标记位置开始的700个数据点
            print(f'截取的数据形状：{sub_data.shape}')
            for channel in channels:
                # 对数据进行下采样
                downsampled_data = DataFilter.perform_downsampling(data[channel], 2, AggOperations.MEDIAN)
                # 计算功率谱
                pxx, frequency = DataFilter.get_psd_welch(downsampled_data, psd_size, psd_size // 2,
                                                          sampling_rate, WindowOperations.BLACKMAN_HARRIS.value)
                print(f'通道 {channel} 的功率谱计算完成')

    # 结束接收
    board.stop_stream()
    board.release_all_sessions()

if __name__ == '__main__':
    init()
    main1()
    # main2()
    pass