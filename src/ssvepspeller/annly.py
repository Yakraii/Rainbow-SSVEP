import numpy as np 
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations
from scipy import signal
from matplotlib import pyplot as plt
import scipy
import os 
samplate = 250
files = os.listdir('./test_data')
data = np.loadtxt('./data/BrainFlow-RAW_2023-10-27_21-37-53_0.csv')
data = data.T
print(data.shape)
eeg_data = data[1:33]
label = data[-1]
label = label[label!= 0]
print(label)
for file in files:
    if 'data' in file:
        continue
    data = np.loadtxt('./test_data/'+ file).T
    labels = data[-2]
    eeg_data = data[[1,2,3]]

    for channel in range(len(eeg_data)):
        DataFilter.detrend(eeg_data[channel], DetrendOperations.NO_DETREND.value)
        DataFilter.perform_bandpass(eeg_data[channel], samplate, 2, 40, 2,
                                            FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_bandstop(eeg_data[channel], samplate, 48, 52, 2,
                                            FilterTypes.BUTTERWORTH.value, 0)
   
    
    mean_data = np.mean(eeg_data, axis=0) / 3
    eeg_data -= mean_data
    freqs = []
    pxxs = []
    samplate = 250
    down_sample= 250
    for index in range(len(labels)):
        label = labels[index]
        if label !=0 :
            subData = eeg_data[:, index+0: index+5*samplate]
            subData = np.mean(subData, axis=0)
            subData = scipy.signal.resample(subData, down_sample*5)
            [freq, pxx] = signal.welch(subData, down_sample, nperseg=5*down_sample, average="median", window='hann')
            freq = freq[40:120]
            pxx = pxx[40: 120]
            print(np.max(pxx), freq[np.where(pxx == np.max(pxx))])
            plt.plot(freq, pxx)
            plt.show()

            freqs.append(freq)
            pxxs.append(pxx)

    fig, axs = plt.subplots(2, 2)

    axs[0, 0].plot(freqs[2], pxxs[2], 'tab:grey')
    axs[0, 0].set_title('H fft' +str( freqs[2][np.where(pxxs[2] == np.max(pxxs[2]))]) + 'HZ')

    axs[0, 1].plot(freqs[5], pxxs[5], 'tab:orange')
    axs[0, 1].set_title('B fft' + str(freqs[4][np.where(pxxs[4] == np.max(pxxs[4]))]) + 'HZ')

    axs[1, 0].plot(freqs[7], pxxs[7], 'tab:green')
    axs[1, 0].set_title('C fft' + str(freqs[8][np.where(pxxs[8] == np.max(pxxs[8]))]) + 'HZ')

    axs[1, 1].plot(freqs[10], pxxs[10], 'tab:red')
    axs[1, 1].set_title('I fft' + str(freqs[11][np.where(pxxs[11] == np.max(pxxs[11]))]) + 'HZ')
    fig.tight_layout()

    # 显示所有子图
    plt.show()

