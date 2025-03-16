import argparse
import json
import numpy as np
import Utils.EEGDataset as EEGDataset
from sklearn.metrics import confusion_matrix
from Model import CCA
from Utils import Ploter

'''                Fs    Nc     Nh     Nf     Ns 
           Dial:  250    8     25     5    1  
'''
parser = argparse.ArgumentParser()
parser.add_argument('--file_name', type=str, default='', help="name of the dataset")
parser.add_argument('--dataset', type=str, default='Dial', help="12-class dataset")
parser.add_argument('--ws', type=float, default=1.0, help="window size of ssvep")
parser.add_argument('--Kf', type=int, default=1, help="k-fold cross validation")
parser.add_argument('--Nh', type=int, default=180, help="number of trial")
parser.add_argument('--Nc', type=int, default=8, help="number of channel")
parser.add_argument('--Fs', type=int, default=256, help="frequency of sample")
parser.add_argument('--Nt', type=int, default=512, help="number of sample")
parser.add_argument('--Nf', type=int, default=12, help="number of stimulus")
parser.add_argument('--Ns', type=int, default=10, help="number of subjects")
parser.add_argument('--UD', type=int, default=-1, help="-1(Unsupervised),0(User-dependent),1(User-Indepedent)")
parser.add_argument('--ratio', type=int, default=-1, help="-1(Training-free),0(N-1vs1),1(8vs2),2(5v5),3(2v8)")

opt = parser.parse_args()

# 设置人数、折叠为1
opt.ws = 3.5
opt.Nh = 25
opt.Fs = 250
opt.Ns = 1
opt.Kf = 1
opt.Nf = 5

# 2、Start Train
final_acc_list = []  # 存储最终准确率的列表
for fold_num in range(opt.Kf):  # 遍历每个折叠
    final_valid_acc_list = []  # 存储每个折叠的验证准确率列表
    print(f"Training for K_Fold {fold_num + 1}")  # 打印当前折叠的训练信息
    for subject in range(1, opt.Ns + 1):  # 遍历每个受试者
        train_dataset = EEGDataset.getSSVEP12Intra(subject, file_name = opt.file_name, train_ratio=0.0, mode="train")  # 获取训练数据集
        test_dataset = EEGDataset.getSSVEP12Intra(subject, file_name = opt.file_name, train_ratio=0.0, mode="test")  # 获取测试数据集

        eeg_train, label_train = train_dataset[:]  # 获取训练数据和标签
        eeg_test, label_test = test_dataset[:]  # 获取测试数据和标签
        eeg_train = eeg_train[:, :, :, :int(opt.Fs * opt.ws)]  # 根据窗口大小裁剪训练数据，256*1=256
        eeg_test = eeg_test[:, :, :, :int(opt.Fs * opt.ws)]  # 根据窗口大小裁剪测试数据

        # 去除空维度，空维度用以表示批次，此处不需要
        eeg_train = eeg_train.squeeze(1).numpy()  # 去除空维度并转换为numpy数组
        eeg_test = eeg_test.squeeze(1).numpy()  # 去除空维度并转换为numpy数组

        # -----------------------------------------------------------------------------------------------------------
        print("eeg_train.shape:", eeg_train.shape)  # 打印训练数据的形状
        print("eeg_test.shape:", eeg_test.shape)  # 打印测试数据的形状
        cca = CCA.CCA_Base(opt=opt)  # 初始化CCA模型
        targets = [7.5, 9.75, 10.25, 12.25, 14.25]


        labels, predicted_labels,average_scores = cca.cca_classify(targets, eeg_test, train_data=eeg_train, template=False)  # 进行CCA分类
        
        # print("labels:", labels)
        # print("predicted_labels:", predicted_labels)

        c_mat = confusion_matrix(labels, predicted_labels)  # 计算混淆矩阵
        accuracy = np.divide(np.trace(c_mat), np.sum(np.sum(c_mat)))  # 计算分类准确率
        print(f'Subject: {subject}, Classification Accuracy:{accuracy:.3f}')  # 打印当前受试者的分类准确率
        final_valid_acc_list.append(accuracy)  # 将当前受试者的准确率添加到验证准确率列表中

    result = {
        # "labels": labels.tolist(),
        "average_scores": average_scores,
        "final_valid_acc_list": final_valid_acc_list # 每个受试者的准确率
        }
    
    print("RESULT:", json.dumps(result))  # 使用 RESULT: 标识 JSON 数据
    final_acc_list.append(final_valid_acc_list)  # 将当前折叠的验证准确率列表添加到最终准确率列表中

# 3、Plot result
Ploter.plot_save_Result(final_acc_list, model_name='CCA', dataset=opt.dataset, UD=opt.UD, ratio=opt.ratio,
                        win_size=str(opt.ws), text=True)  # 绘制并保存结果


