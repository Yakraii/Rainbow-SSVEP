import pandas as pd
import numpy as np
import scipy.io
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations, AggOperations


# 预处理函数（保持不变）
def process(channels, origin_sampling_rate):
    downsampled_data = []
    for ch in range(8):
        channel_data = channels[:, ch]
        DataFilter.detrend(channel_data, DetrendOperations.CONSTANT.value)
        DataFilter.perform_bandpass(channel_data, origin_sampling_rate, 3.0, 45.0, 4, FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandstop(channel_data, origin_sampling_rate, 48.0, 52.0, 2, FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandstop(channel_data, origin_sampling_rate, 58.0, 62.0, 2, FilterTypes.BUTTERWORTH.value, 0)
        downsampled_ch = DataFilter.perform_downsampling(channel_data, 4, AggOperations.MEAN.value)
        downsampled_data.append(downsampled_ch)
    return np.array(downsampled_data).T


# 参数设置
origin_sampling_rate = 1000
target_sampling_rate = 250
total_duration = 20  # 秒
segment_duration = 4  # 秒
n_segments = 5
required_samples = target_sampling_rate * total_duration  # 5000

# 定义CSV文件路径及其对应的频率
files = [
    {'path': 'data/7.5&10.csv', 'freqs': [7.5, 10], 'keep_freqs': [7.5]},
    {'path': 'data/9.75&14.25.csv', 'freqs': [9.75, 14.25], 'keep_freqs': [9.75, 14.25]},
    {'path': 'data/12.25&10.25.csv', 'freqs': [12.25, 10.25], 'keep_freqs': [12.25, 10.25]}
]

all_freq_data = {}  # 存储所有频率数据

for file_info in files:
    df = pd.read_csv(file_info['path'])
    freq1, freq2 = file_info['freqs']
    keep_freqs = file_info['keep_freqs']

    # 处理每个频率对应的标记（1和2）
    for marker, freq in [(1, freq1), (2, freq2)]:
        if freq not in keep_freqs:
            continue
        indices = []
        for idx, row in df.iterrows():
            if row['marker'] == marker:
                indices.append(idx)

        # 检查成对的标记
        if len(indices) % 2 != 0:
            indices = indices[:-1]
        if not indices:
            continue

        # 合并所有实验段数据
        combined_data = []
        for i in range(0, len(indices), 2):
            segment = df.iloc[indices[i] + 1: indices[i + 1]]
            combined_data.append(segment)
        combined_df = pd.concat(combined_data)

        # 提取通道数据并处理
        channels = combined_df[[f'channel_{i + 1}' for i in range(8)]].values
        processed = process(channels, origin_sampling_rate)

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

        # 保存频率数据
        if freq not in all_freq_data:
            all_freq_data[freq] = []
        all_freq_data[freq].append(final_segments)

# 合并所有频率数据并按升序排列
sorted_freqs = sorted(all_freq_data.keys())
output = []
for freq in sorted_freqs:
    freq_segments = np.concatenate(all_freq_data[freq], axis=2)
    output.append(freq_segments[:, :, :5])  # 确保每个频率取5段

output = np.stack(output, axis=0)
print("输出形状:", output.shape)  # (6, 8, 1000, 5)

# 保存结果
scipy.io.savemat('data/processed_data.mat', {'processed_data': output})