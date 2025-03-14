# 设计者:潘宇东
# 编码者:上帝之手
# 时间:2021/10/6 22:47
import numpy as np
from torch.utils.data import Dataset
import torch
import scipy.io
from scipy import signal

# 定义一个继承自Dataset的类getSSVEP12Intra
class getSSVEP12Intra(Dataset):
    # 初始化方法
    def __init__(self, subject=1, train_ratio=0.8, KFold=None, n_splits=5, mode="train"):
        super(getSSVEP12Intra, self).__init__()
        self.train_ratio = train_ratio  # 训练集比例
        self.Nh = 180  # 总样本数
        self.Nc = 8  # 通道数
        self.Nt = 1024  # 每个样本的时间点数
        self.Nf = 12  # 频率数
        self.Fs = 256  # 采样率
        self.subject = subject  # 被试编号
        self.eeg_data, self.label_data = self.load_Data()  # 加载数据
        self.num_trial = self.Nh // self.Nf  # 每个频率的试验数
        self.train_idx = []  # 训练集索引
        self.test_idx = []  # 测试集索引
        if KFold is not None:
            fold_trial = self.num_trial // n_splits  # 每折的试验数
            self.valid_trial_idx = [i for i in range(KFold * fold_trial, (KFold + 1) * fold_trial)]  # 验证集索引

        for i in range(0, self.Nh, self.Nh // self.Nf):  # 遍历每个频率的起始索引
            for j in range(self.Nh // self.Nf):  # 遍历每个频率的试验
                if n_splits == 2 and j == self.num_trial - 1:  # 如果是2折交叉验证且是最后一个试验，跳过
                    continue
                if KFold is not None:
                    if j not in self.valid_trial_idx:
                        self.train_idx.append(i + j)  # 添加到训练集索引
                    else:
                        self.test_idx.append(i + j)  # 添加到测试集索引
                else:
                    if j < int(self.num_trial * train_ratio):
                        self.train_idx.append(i + j)  # 添加到训练集索引
                    else:
                        self.test_idx.append(i + j)  # 添加到测试集索引

        self.eeg_data_train = self.eeg_data[self.train_idx]  # 训练集EEG数据
        self.label_data_train = self.label_data[self.train_idx]  # 训练集标签数据
        self.eeg_data_test = self.eeg_data[self.test_idx]  # 测试集EEG数据
        self.label_data_test = self.label_data[self.test_idx]  # 测试集标签数据

        if mode == 'train':
            self.eeg_data = self.eeg_data_train  # 训练模式下使用训练集数据
            self.label_data = self.label_data_train
        elif mode == 'test':
            self.eeg_data = self.eeg_data_test  # 测试模式下使用测试集数据
            self.label_data = self.label_data_test

        print(f'eeg_data for subject {subject}:', self.eeg_data.shape)
        print(f'label_data for subject {subject}:', self.label_data.shape)

    # 获取数据项
    def __getitem__(self, index):
        return self.eeg_data[index], self.label_data[index]

    # 获取数据长度
    def __len__(self):
        return len(self.label_data)

    # 加载单个被试的数据
    def load_Data(self):
        subjectfile = scipy.io.loadmat(f'data/Dial/S{self.subject}.mat')  # 加载.mat文件
        samples = subjectfile['eeg']  # 获取EEG数据 (12, 8, 1024, 15)
        eeg_data = samples[0, :, :, :]  # 初始化EEG数据 (8, 1024, 15)
        for i in range(1, 12):
            eeg_data = np.concatenate([eeg_data, samples[i, :, :, :]], axis=2)  # 拼接数据
        eeg_data = eeg_data.transpose([2, 0, 1])  # 转置数据 (180, 8, 1024)
        eeg_data = np.expand_dims(eeg_data, axis=1)  # 扩展维度 (180, 1, 8, 1024)
        eeg_data = torch.from_numpy(eeg_data)  # 转换为Tensor
        label_data = np.zeros((180, 1))  # 初始化标签数据
        for i in range(12):
            label_data[i * 15:(i + 1) * 15] = i  # 设置标签
        label_data = torch.from_numpy(label_data)  # 转换为Tensor
        print(eeg_data.shape)
        print(label_data.shape)
        return eeg_data, label_data  # 返回EEG数据和标签数据
