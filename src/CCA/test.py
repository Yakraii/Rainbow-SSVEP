import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, fftfreq

# 参数设置
Fs = 1000  # 采样率 (Hz)
stim_freqs = np.arange(8, 16, 0.1)  # 刺激频率 (8Hz到15Hz，步长1Hz)
nfft = 8 * Fs  # FFT点数 (提高分辨率)
window = signal.windows.hann(Fs * 4)  # 汉宁窗 (增加窗长)

# 模拟生成SSVEP数据 (替换为实际数据)
def generate_ssvep_data(stim_freq, duration=4):
    t = np.arange(0, duration, 1/Fs)
    signal_clean = 0.5 * np.sin(2 * np.pi * stim_freq * t)  # 基频
    for harmonic in range(2, 9):  # 添加2次到8次谐波
        signal_clean += (0.5 / harmonic) * np.sin(2 * np.pi * harmonic * stim_freq * t)
    noise = 0.1 * np.random.normal(size=len(t))  # 添加噪声
    return signal_clean + noise

# 数据预处理与频谱计算
def compute_psd(data, Fs, nfft):
    freqs, psd = signal.welch(data, fs=Fs, window=window, nperseg=len(window),
                             noverlap=Fs//2, nfft=nfft, scaling='spectrum')
    return freqs, psd

# 构建刺激-响应频率矩阵
resp_freqs = np.arange(0, 100, 0.25)  # 响应频率范围 (0-100Hz，分辨率0.25Hz)
power_matrix = np.zeros((len(stim_freqs), len(resp_freqs)))

for i, stim_freq in enumerate(stim_freqs):
    # 生成模拟数据 (替换为实际EEG数据)
    eeg_data = generate_ssvep_data(stim_freq)
    
    # 计算功率谱密度
    freqs, psd = compute_psd(eeg_data, Fs, nfft)
    
    # 插值到统一频率网格
    power_matrix[i, :] = np.interp(resp_freqs, freqs, psd)

# 绘制热力图
plt.figure(figsize=(12, 6))
plt.imshow(10 * np.log10(power_matrix), aspect='auto', origin='lower',
           extent=[resp_freqs[0], resp_freqs[-1], stim_freqs[0], stim_freqs[-1]],
           cmap='jet', vmin=-50, vmax=0)  # 设置色标范围
plt.colorbar(label='Power Spectral Density (dB)')
plt.xlabel('Response Frequency (Hz)')
plt.ylabel('Stimulus Frequency (Hz)')
plt.title('SSVEP Stimulus-Response Frequency Analysis (8-15 Hz Stimulus)')

# 标注谐波位置
for stim_freq in stim_freqs:
    for harmonic in range(1, 9):  # 标注基频到8次谐波
        resp_freq = stim_freq * harmonic
        if resp_freq <= resp_freqs[-1]:
            plt.plot(resp_freq, stim_freq, 'wo', markersize=8, markeredgecolor='k')

plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()