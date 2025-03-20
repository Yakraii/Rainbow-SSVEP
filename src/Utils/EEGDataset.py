import numpy as np
from torch.utils.data import Dataset
import torch
import scipy.io
from scipy import signal
import os
from module import getPath
# 读取路径
root_path = getPath.getRootPath()
data_path = os.path.join(root_path, 'data', 'data_processed')

# 定义一个继承自Dataset的类getSSVEP12Intra
class getSSVEP12Intra(Dataset):
    # 初始化方法
    def __init__(self,  subject=1, file_name = "merged_data", train_ratio=0.8, KFold=None, n_splits=5, mode="train"):
        super(getSSVEP12Intra, self).__init__()
        self.file_name = file_name
        self.train_ratio = train_ratio  # 训练集比例
        self.Nh = 25  # 总样本数
        self.Nc = 8  # 通道数
        self.Nt = 1000  # 每个样本的时间点数
        self.Nf = 5  # 频率数
        self.Fs = 250  # 采样率
        self.subject = subject  # 被试编号
        self.eeg_data, self.label_data = self.load_Data()  # 加载数据
        self.num_trial = self.Nh // self.Nf  # 每个频率的试验数
        self.train_idx = []  # 训练集索引
        self.test_idx = []  # 测试集索引

        for i in range(0, self.Nh, self.num_trial):  # 遍历每个频率的起始索引
            for j in range(self.num_trial):  # 遍历每个频率的试验
                if n_splits == 2 and j == self.num_trial - 1:  # 如果是2折交叉验证且是最后一个试验，跳过
                    continue

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
        # subjectfile = scipy.io.loadmat(f'data/Dial/S{self.subject}.mat')  # 加载.mat文件
        subjectfile = scipy.io.loadmat(os.path.join(data_path, self.file_name) + ".mat")  # 加载.mat文件
        print("数据集路径：",os.path.join(data_path, self.file_name) + ".mat")
        # print(subjectfile.keys())
        samples = subjectfile['processed_data']  # 获取EEG数据 (12, 8, 1024, 15)
        # samples = samples[:2, :, :, :] # 将samples中的第一维删至 (2, 8, 1024, 15)

        eeg_data = samples[0, :, :, :]  # 初始化EEG数据 (8, 1024, 15)
        for i in range(1, 5):
            eeg_data = np.concatenate([eeg_data, samples[i, :, :, :]], axis=2)  # 拼接数据
        eeg_data = eeg_data.transpose([2, 0, 1])  # 转置数据 (180, 8, 1024)
        eeg_data = np.expand_dims(eeg_data, axis=1)  # 扩展维度 (180, 1, 8, 1024)
        eeg_data = torch.from_numpy(eeg_data)  # 转换为Tensor
        # label_data = np.zeros((180, 1))  # 初始化标签数据
        label_data = np.zeros((self.Nh, 1))  # 初始化标签数据
        for i in range(5):
            label_data[i * 5:(i + 1) * 5] = i  # 设置标签
        label_data = torch.from_numpy(label_data)  # 转换为Tensor
        print("eeg_data.shape: ",eeg_data.shape)
        print("label_data.shape: ",label_data.shape)
        return eeg_data, label_data  # 返回EEG数据和标签数据
