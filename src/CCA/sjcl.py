import pandas as pd
import numpy as np
import scipy.io
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations, WindowOperations, AggOperations
from matplotlib import pyplot as plt

def draw(data_x, data_y):
    start_index = len(data_x) // 2 - 500  # 中间位置往前 500 个点
    end_index = len(data_x) // 2 + 500  # 中间位置往后 500 个点
    data_x = data_x[start_index:end_index]
    data_y = data_y[start_index:end_index]
    # 设置图形大小
    plt.figure(figsize=(10, 6))  # 调整图形大小
    # 绘制折线图
    plt.plot(data_x, data_y, linestyle='-', linewidth=1, color='b', marker='', label='Data')
    # 添加标题和标签
    plt.title('Line Plot with Many Data Points')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    # 显示图例
    plt.legend()
    # 显示图形
    plt.show()

# 预处理
def process(channels, origin_sampling_rate):
    downsampled_data = []
    for ch in range(8):
        channel_data = channels[:, ch]
        # 去趋势 + 滤波（在原始 1000Hz 上操作）
        DataFilter.detrend(channel_data, DetrendOperations.CONSTANT.value)
        DataFilter.perform_bandpass(channel_data, origin_sampling_rate, 3.0, 20.0, 4, FilterTypes.BUTTERWORTH.value,
                                    0)
        DataFilter.perform_bandstop(channel_data, origin_sampling_rate, 48.0, 52.0, 2,
                                    FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandstop(channel_data, origin_sampling_rate, 58.0, 62.0, 2,
                                    FilterTypes.BUTTERWORTH.value, 0)
        data_x = [j for j in range(len(channel_data))]
        data_y = channel_data

        # draw(data_x, data_y)
        # 降采样（均值法）
        downsampled_ch = DataFilter.perform_downsampling(channel_data, 4, AggOperations.MEAN.value)
        downsampled_data.append(downsampled_ch)

    # 转换为 numpy 数组并转置为 (samples, channels)
    downsampled_data = np.array(downsampled_data).T
    return downsampled_data

# 读取 CSV 文件
df = pd.read_csv('data/7.5&10.csv')

# 提取标志位为 1 和 2 的索引位置
marker_indices = {1: [], 2: []}
for idx, row in df.iterrows():
    if row['marker'] in [1, 2]:
        marker_indices[row['marker']].append(idx)

# 定义存储实验段的字典 (key=频率, value=数据列表)
experiment_segments = {1: [], 2: []}

# 处理每个频率的标志位
for freq in [1, 2]:
    indices = marker_indices[freq]
    # 必须成对出现（开始和结束）
    if len(indices) % 2 != 0:
        print(f"警告：频率 {freq} 的标志位不成对，跳过未闭合的段")
        indices = indices[:-1]  # 忽略最后一个未闭合的标记

    # 按每对标志位截取数据
    for i in range(0, len(indices), 2):
        start_idx = indices[i]
        end_idx = indices[i + 1]
        segment_data = df.iloc[start_idx + 1: end_idx]  # 不包含标志位行
        experiment_segments[freq].append(segment_data)

origin_sampling_rate = 1000
target_sampling_rate = 250
total_duration = 20  # 秒
segment_duration = 4  # 秒
n_segments = 5
required_samples = target_sampling_rate * total_duration  # 5120->5000

# 初始化存储结构 (2频率, 8通道, 1024样本点, 5段)
final_data = {1: [], 2: []}

for freq in [1, 2]:
    for segment_df in experiment_segments[freq]:
        # 提取 8 个通道数据（假设列名为 channel_1 到 channel_8）
        channels = segment_df[['channel_1', 'channel_2', 'channel_3', 'channel_4',
                               'channel_5', 'channel_6', 'channel_7', 'channel_8']].values

        # 基线漂移处理+滤波+降采样
        # 统一处理滤波，去趋势
        # 降采样到 250Hz（实际 1000/4=250，接近目标 256Hz）
        channels = process(channels, origin_sampling_rate)

        # 检查数据长度
        if len(channels) < required_samples:
            print(f"频率 {freq} 的某段数据不足 20 秒，进行零填充")
            padding = required_samples - len(channels)
            channels = np.pad(channels, ((0, padding), (0, 0)), mode='constant')

        # 截取中间 20 秒（5120->5000 样本点）
        start = (len(channels) - required_samples) // 2
        end = start + required_samples
        trimmed_data = channels[start:end]

        # 分割为 5 段，每段 4 秒（1024 样本点）
        # segments_split = np.array_split(trimmed_data, n_segments)
        segments_split = [trimmed_data[i * 1000: (i + 1) * 1000] for i in range(n_segments)]
        segments_transposed = np.stack(segments_split, axis=2).transpose(1, 0, 2)

        final_data[freq].append(segments_transposed)

    # 合并同一频率的所有段
    if final_data[freq]:
        final_data[freq] = np.concatenate(final_data[freq], axis=2)
    else:
        final_data[freq] = np.zeros((8, 1000, 0))  # 无数据时填充空数组

# 组合为最终格式 (2, 8, 1024, 5)
output = np.stack([final_data[1], final_data[2]], axis=0)
print("输出形状:", output.shape)  # 应为 (2, 8, 1024, N)，其中 N 是有效段数


# 将处理结果保存为mat文件
# 定义保存的文件路径
save_path = 'data/7.5&10.mat'

# 使用 savemat 函数保存数据
scipy.io.savemat(save_path, {'processed_data': output})

print(f"处理结果已保存为 {save_path}")