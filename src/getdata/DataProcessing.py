import pandas as pd
import numpy as np
import scipy.io
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations, AggOperations
import argparse

# 读取CSV文件函数
def read_csv(file_path):
    return pd.read_csv(file_path)

def combine_data(data, marker): # 合并数据，返回通道数据
    indices = []
    for idx, row in data.iterrows():
        if row['marker'] == marker:
            indices.append(idx)

    # 合并所有实验段数据
    combined_data = []
    for i in range(0, len(indices), 2):
        segment = data.iloc[indices[i] + 1: indices[i + 1]]
        combined_data.append(segment)
    combined_df = pd.concat(combined_data)

    # 提取通道数据并处理
    channels = combined_df[[f'channel_{i + 1}' for i in range(8)]].values
    return channels

def process_data(channels, freq): # 处理数据
    downsampled_data = []
    for ch in range(8):
        channel_data = channels[:, ch]
        DataFilter.detrend(channel_data, DetrendOperations.CONSTANT.value)
        DataFilter.perform_bandpass(channel_data, origin_sampling_rate, 3.0, 45.0, 4, FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandstop(channel_data, origin_sampling_rate, 48.0, 52.0, 2, FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandstop(channel_data, origin_sampling_rate, 58.0, 62.0, 2, FilterTypes.BUTTERWORTH.value, 0)
        downsampled_ch = DataFilter.perform_downsampling(channel_data, 4, AggOperations.MEAN.value)
        downsampled_data.append(downsampled_ch)
        processed = np.array(downsampled_data).T

    # 填充和截取中间20秒
    if len(processed) < required_samples:
        print(f"频率 {freq} 的某段数据不足 20 秒，进行零填充")
        pad = required_samples - len(processed)
        processed = np.pad(processed, ((0, pad), (0, 0)), mode='constant')
    start = (len(processed) - required_samples) // 2
    trimmed = processed[start: start + required_samples]

    # 分割为5段
    segments = [trimmed[i * 1000:(i + 1) * 1000] for i in range(n_segments)]
    final_segments = np.stack(segments, axis=2).transpose(1, 0, 2)
    return final_segments

def save_data(all_freq_data):
    # 合并所有频率数据并按升序排列
    sorted_freqs = sorted(all_freq_data.keys())
    output = []
    for freq in sorted_freqs:
        freq_segments = np.concatenate(all_freq_data[freq], axis=2)
        output.append(freq_segments[:, :, :5])  # 确保每个频率取5段

    output = np.stack(output, axis=0)
    print("输出形状:", output.shape)  # (6, 8, 1000, 5)

    # 保存结果
    scipy.io.savemat('../../data/' + args.file_path + ".mat", {'processed_data': output})

if __name__ == '__main__':
    # 接收两个个参数：csv文件地址、频率1
    parser = argparse.ArgumentParser(description="Data processing script.")
    parser.add_argument('--file_path', type=str, default="", help='Path to the rawDa CSV file')
    parser.add_argument('--frequencies', type=float, nargs='*', default=[9.75,14.25], help='List of frequencies')
    
    args = parser.parse_args()
    frequency = args.frequencies
    print(args)

    # 参数设置
    origin_sampling_rate = 1000  # 原始采样率
    target_sampling_rate = 250  # 目标采样率
    total_duration = 20  # 秒
    segment_duration = 4  # 秒
    n_segments = 5  # 段数
    required_samples = target_sampling_rate * total_duration  # 5000

    all_freq_data = {}  # 存储所有频率数据

    data = read_csv(args.file_path)  # 读取CSV文件
    # 处理每个频率对应的标记
    # for marker, freq in [(1, frequency[0]), (2, frequency[1]), (3, frequency[2]), (4, frequency[3])]:
    for marker, freq in [(1, frequency[0]), (2, frequency[1])]:
        channels = combine_data(data, marker) # 合并数据，返回通道数据
        processed_data = process_data(channels, freq) # 处理数据
        # 保存频率数据
        if freq not in all_freq_data:
            all_freq_data[freq] = []
        all_freq_data[freq].append(processed_data)
    save_data(all_freq_data) # 保存数据


# all_freq_data = {}  # 存储所有频率数据
#
# for file_info in files:
#     df = pd.read_csv(file_info['path'])
#     freq1, freq2 = file_info['freqs']
#     keep_freqs = file_info['keep_freqs']
#
#     # 处理每个频率对应的标记（1和2）
#     for marker, freq in [(1, freq1), (2, freq2)]:
#         if freq not in keep_freqs:
#             continue
#         indices = []
#         for idx, row in df.iterrows():
#             if row['marker'] == marker:
#                 indices.append(idx)
#
        # # 检查成对的标记
        # if len(indices) % 2 != 0:
        #     indices = indices[:-1]
        # if not indices:
        #     continue
#
#         # 合并所有实验段数据
#         combined_data = []
#         for i in range(0, len(indices), 2):
#             segment = df.iloc[indices[i] + 1: indices[i + 1]]
#             combined_data.append(segment)
#         combined_df = pd.concat(combined_data)
#
#         # 提取通道数据并处理
#         channels = combined_df[[f'channel_{i + 1}' for i in range(8)]].values
#         processed = process(channels, origin_sampling_rate)
#
#         # 填充和截取中间20秒
#         if len(processed) < required_samples:
#             print(f"频率 {freq} 的某段数据不足 20 秒，进行零填充")
#             pad = required_samples - len(processed)
#             processed = np.pad(processed, ((0, pad), (0, 0)), mode='constant')
#         start = (len(processed) - required_samples) // 2
#         trimmed = processed[start: start + required_samples]
#
#         # 分割为5段
#         segments = [trimmed[i * 1000:(i + 1) * 1000] for i in range(n_segments)]
#         final_segments = np.stack(segments, axis=2).transpose(1, 0, 2)
#
#         # 保存频率数据
#         if freq not in all_freq_data:
#             all_freq_data[freq] = []
#         all_freq_data[freq].append(final_segments)
#
# # 合并所有频率数据并按升序排列
# sorted_freqs = sorted(all_freq_data.keys())
# output = []
# for freq in sorted_freqs:
#     freq_segments = np.concatenate(all_freq_data[freq], axis=2)
#     output.append(freq_segments[:, :, :5])  # 确保每个频率取5段
#
# output = np.stack(output, axis=0)
# print("输出形状:", output.shape)  # (6, 8, 1000, 5)
#
# # 保存结果
# scipy.io.savemat('data/processed_data.mat', {'processed_data': output})
#
#
