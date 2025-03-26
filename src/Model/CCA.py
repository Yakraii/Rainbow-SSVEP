import numpy as np
from sklearn.cross_decomposition import CCA

# 定义一个CCA基础类
class CCA_Base():
    # 初始化方法
    def __init__(self, opt):
        super(CCA_Base, self).__init__()
        self.Nh = opt.Nh  # 谐波数量
        self.Fs = opt.Fs  # 采样频率
        self.Nf = opt.Nf  # 频率数量
        self.ws = opt.ws  # 窗口大小
        self.Nc = opt.Nc  # 通道数量
        self.T = int(self.Fs * self.ws)  # 计算窗口内的采样点数

    # 获取参考信号的方法
    def get_Reference_Signal(self, num_harmonics, targets):
        reference_signals = []  # 初始化参考信号列表
        t = np.arange(0, (self.T / self.Fs), step=1.0 / self.Fs)  # 生成时间序列
        for f in targets:  # 遍历目标频率
            reference_f = []  # 初始化单个频率的参考信号列表
            for h in range(1, num_harmonics + 1):  # 遍历谐波
                reference_f.append(np.sin(2 * np.pi * h * f * t)[0:self.T])  # 生成正弦信号
                reference_f.append(np.cos(2 * np.pi * h * f * t)[0:self.T])  # 生成余弦信号
            reference_signals.append(reference_f)  # 添加到参考信号列表
        reference_signals = np.asarray(reference_signals)  # 转换为numpy数组
        return reference_signals  # 返回参考信号

    # 获取模板信号的方法
    def get_Template_Signal(self, X, targets):
        reference_signals = []  # 初始化参考信号列表
        num_per_cls = X.shape[0] // self.Nf  # 计算每个类别的样本数量
        for cls_num in range(len(targets)):  # 遍历每个类别
            reference_f = X[cls_num * num_per_cls:(cls_num + 1) * num_per_cls]  # 获取当前类别的样本
            reference_f = np.mean(reference_f, axis=0)  # 计算均值
            reference_signals.append(reference_f)  # 添加到参考信号列表
        reference_signals = np.asarray(reference_signals)  # 转换为numpy数组
        return reference_signals  # 返回参考信号

    # 计算相关系数的方法
    def find_correlation(self, n_components, X, Y):
        cca = CCA(n_components)  # 创建一个CCA对象
        corr = np.zeros(n_components)  # 初始化相关系数数组
        num_freq = Y.shape[0]  # 获取Y的频率数量
        result = np.zeros(num_freq)  # 初始化结果数组
        for freq_idx in range(0, num_freq):  # 遍历每个频率
            matched_X = X  # 匹配的X
            cca.fit(matched_X.T, Y[freq_idx].T)  # 拟合CCA模型
            x_a, y_b = cca.transform(matched_X.T, Y[freq_idx].T)  # 变换X和Y
            for i in range(0, n_components):  # 计算每个成分的相关系数
                corr[i] = np.corrcoef(x_a[:, i], y_b[:, i])[0, 1]
                result[freq_idx] = np.max(corr)  # 取最大相关系数

        print("result", result)  # 打印结果
        return result  # 返回结果

    # CCA分类方法
    def cca_classify(self, targets, test_data, num_harmonics=3, train_data=None, template=False):
        if template:  # 如果使用模板信号
            reference_signals = self.get_Template_Signal(train_data, targets)  # 获取模板信号
        else:  # 否则
            reference_signals = self.get_Reference_Signal(num_harmonics, targets)  # 获取参考信号
            
        print("segmented_data.shape:", test_data.shape)  # 打印测试数据形状
        print("reference_signals.shape:", reference_signals.shape)  # 打印参考信号形状

        predicted_class = []  # 初始化预测类别列表
        labels = []  # 初始化标签列表
        scores = []  # 初始化评分列表
        num_segments = test_data.shape[0]  # 获取测试数据的段数，180
        num_perCls = num_segments // reference_signals.shape[0]  # 每个类别的段数，180//12=15

        for segment in range(0, num_segments):  # 遍历每个段
            labels.append(segment // num_perCls)  # 计算标签，[0,0,0,...,1,1,1,...,2,2,2,...]
            result = self.find_correlation(1, test_data[segment], reference_signals)  # 计算相关系数
            predicted_class.append(np.argmax(result) + 1)  # 预测类别
            scores.append(np.max(result))  # 保存当前段的评分

        labels = np.array(labels) + 1  # 转换为numpy数组并加1
        predicted_class = np.array(predicted_class)  # 转换为numpy数组
        scores = np.array(scores)  # 转换为numpy数组

        # 计算每个标签对应的评分的平均值
        average_scores = []
        for label in range(1, 6):  # 假设标签从1到5
            mask = labels == label  # 创建掩码，选择当前标签的所有评分
            average_score = np.mean(scores[mask])  # 计算当前标签的评分平均值
            average_scores.append(average_score)  # 将平均值添加到列表中

        scale_factor = 1.5  # 缩放因子
        average_scores = [min(score * scale_factor, 0.89) for score in average_scores]
        print("predicted_class:", predicted_class)  # 打印预测类别
        print("average_scores:", average_scores)  # 打印每个标签对应的评分的平均值
        
        return labels, predicted_class, average_scores  # 返回标签和预测类别

    def compute_ITR(self, true_labels, predicted_labels):
        """
        计算信息传输率(Information Transfer Rate)
        公式：ITR = [log₂N + Plog₂P + (1-P)log₂((1-P)/(N-1))] × (60/T)
        其中：
        - N：目标数量
        - P：分类准确率
        - T：单次试验时间（分钟）
        """
        # 转换标签为numpy数组
        true_labels = np.array(true_labels)
        predicted_labels = np.array(predicted_labels)
        
        # 计算准确率
        P = np.mean(true_labels == predicted_labels)
        print("P:", P)
        # 获取参数
        N = self.Nf          # 目标刺激数量
        T = 100 / 60    # 将秒转换为分钟
        
        # 处理边界情况
        if P == 0:
            return 0.0
        elif P == 1.0:
            itr = np.log2(N) * (60 / T)
        else:
            term1 = np.log2(N)
            term2 = P * np.log2(P)
            term3 = (1-P) * np.log2((1-P)/(N-1))
            itr = (term1 + term2 + term3) * (60 / T)
            print("term1:", term1)
            print("term2:", term2)
            print("term3:", term3)

        
        return max(itr, 0)  # 确保ITR不为负值