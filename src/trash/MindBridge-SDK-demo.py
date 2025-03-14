from brainflow.board_shim import BoardShim , BrainFlowInputParams
from  matplotlib import pyplot as plt 
import time
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations, WindowOperations, AggOperations
# import mne
import scipy
# 获取数据 demo
def main():
    param = BrainFlowInputParams()
    param.ip_address = "192.168.31.41"
    param.ip_port = 9527
    # param.timeout = 1000
    board_id = 532 #5 # 516 # 532 # 564
    board = BoardShim(board_id, param)
    board.prepare_session()
    if board.is_prepared():
        print('adfasdf')
    board.start_stream()
    time.sleep(3)
    board.stop_stream()
    data = board.get_board_data()
    DataFilter.write_file(data, './b.csv', 'w')
    marker = board.get_marker_channel(board_id)
    print(marker)
    label= data[marker]
    print(label)

# 获取数据 实时获取数据
def main():
    param = BrainFlowInputParams()
    print(param)
    param.ip_address = "192.168.31.41"
    param.ip_port = 9527
    param.timeout = 1000
    board_id = 532
    board = BoardShim(board_id, param)
    board.prepare_session()
    if board.is_prepared():
        print('adfasdf')
    board.start_stream()
    data = []
    count = 0
    while count  < 100 :
        time.sleep(1)
        num_se = 2
        sampa_rate = 1000
        current_data = board.get_current_board_data(num_se * sampa_rate)
        # current_data = board.get_board_data()
        print(current_data.shape)
        count += 1
    board.stop_stream()
    board.release_all_sessions()


#实时波形图
def main():
    global board
    param = BrainFlowInputParams()
    param.ip_address = "192.168.31.41"
    param.ip_port = 9527
    param.timeout = 1000
    board_id = 532
    board = BoardShim(board_id, param)
    board.prepare_session()
    if board.is_prepared():
        print('adfasdf')
    board.start_stream()
    count = 0
    ax = plt.axes()
    ax.set_ylim(-500, 500)
    ax.axis('off')
    while count  < 100 :
        ax.cla()
        current_data = board.get_current_board_data(5000)
        data_x = [i for i in range(len(current_data[0]))]
        data_y = current_data[0]
        DataFilter.detrend(data_y, DetrendOperations.CONSTANT.value)
#         #带通滤波
        DataFilter.perform_bandpass(data_y, 1000, 3.0, 45.0, 4,
                                    FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandstop(data_y, 1000, 48.0, 52.0, 2,
                                    FilterTypes.BUTTERWORTH.value, 0)
        ax.plot(data_x, data_y)
        plt.draw()
        plt.pause(0.05)
        count+= 1
    board.stop_stream()
    board.release_all_sessions()


# 数据打标，数据截取
# 1: 注意
# 2： 非注意
def main():
    param = BrainFlowInputParams()
    print(param)
    param.ip_address = "192.168.31.41"
    param.ip_port = 9527
    param.timeout = 1000
    board_id = 532
    board = BoardShim(board_id, param)
    board.prepare_session()
    if board.is_prepared():
        print('adfasdf')
    board.start_stream()
    count = 0
    while count  < 10 :
        time.sleep(1)
        board.insert_marker(count+1)
        current_data = board.get_current_board_data(1000)
        print(current_data.shape)
        count += 1
    marker = board.get_marker_channel(board_id)
    print(marker)
    data = board.get_board_data()
    DataFilter.write_file(data, './marker.csv', 'w')

    print(data.shape)
    labels= data[marker]
    for index in range(len(labels)):
        label = labels[index]
        if label != 0:
            print('label', label, index)
            sub_data = data[:, index: index+ 700]
            print(sub_data.shape)
    board.stop_stream()
    board.release_all_sessions()

# 傅里叶变换， 功率谱计算
# 滤波处理
def main():
    param = BrainFlowInputParams()
    print(param)
    param.ip_address = "192.168.31.56"
    param.ip_port = 9527
    param.timeout = 1000
    board_id = 532
    board = BoardShim(board_id, param)
    board.prepare_session()
    if board.is_prepared():
        print('adfasdf')
    board.start_stream()
    count = 0
    while count  < 10 :
        time.sleep(1)
        board.insert_marker(1)
        current_data = board.get_current_board_data(1000)
        print(current_data.shape)
        count += 1
    board.stop_stream()
    board.release_all_sessions()

    marker = board.get_marker_channel(board_id)
    print(marker)
    data = board.get_board_data()
    labels= data[marker]
    channels= board.get_eeg_channels(board_id)
    sampling_rate = board.get_sampling_rate(board_id)
    for count, channel in enumerate(channels):
        # plot timeseries
        # 基线漂移处理
        DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
        #带通滤波
        DataFilter.perform_bandpass(data[channel], sampling_rate, 3.0, 45.0, 4,
                                    FilterTypes.BUTTERWORTH.value, 0)
        #带阻滤波
        DataFilter.perform_bandstop(data[channel], sampling_rate, 48.0, 52.0, 2,
                                    FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandstop(data[channel], sampling_rate, 58.0, 62.0, 2,
                                            FilterTypes.BUTTERWORTH.value, 0)


def main():
    param = BrainFlowInputParams()
    print(param)
    param.ip_address = "192.168.31.56"
    param.ip_port = 9527
    param.timeout = 1000
    board_id = 532
    board = BoardShim(board_id, param)
    board.prepare_session()
    if board.is_prepared():
        print('adfasdf')
    board.start_stream()
    count = 0
    while count  < 10 :
        time.sleep(1)
        board.insert_marker(1)
        current_data = board.get_current_board_data(1000)
        print(current_data.shape)
        count += 1
    marker = board.get_marker_channel(board_id)
    print(marker)
    data = board.get_board_data()
    labels= data[marker]
    channels= board.get_eeg_channels(board_id)
    sampling_rate = board.get_sampling_rate(board_id)
    for count, channel in enumerate(channels):
        # plot timeseries
        # 基线漂移处理
        DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
        #带通滤波
        DataFilter.perform_bandpass(data[channel], sampling_rate, 3.0, 45.0, 2,
                                    FilterTypes.BUTTERWORTH.value, 0)
        #带阻滤波
        DataFilter.perform_bandstop(data[channel], sampling_rate, 48.0, 52.0, 2,
                                    FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandstop(data[channel], sampling_rate, 58.0, 62.0, 2,
                                            FilterTypes.BUTTERWORTH.value, 0)
    psd_size = DataFilter.get_nearest_power_of_two(sampling_rate)
    for index in range(len(labels)):
        label = labels[index]
        if label != 0:
            print('label', label, index)
            sub_data = data[:, index: index+ 700]
            print(sub_data.shape)
            # 对数据进行功率谱计算
            for count, channel in enumerate(channels):
                sub_data = DataFilter.perform_downsampling(data[channel], 2, AggOperations.MEDIAN)
                pxx ,frquenc  = DataFilter.get_psd_welch(data[channel], psd_size, psd_size // 2,
                                                    sampling_rate,
                                                    WindowOperations.BLACKMAN_HARRIS.value)
    board.stop_stream()
    board.release_all_sessions()

if __name__ == '__main__':
    main()