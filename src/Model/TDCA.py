import numpy as np
from scipy.linalg import qr
from scipy.stats import pearsonr
from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin
from scipy import signal
from scipy.linalg import eigh
from scipy.linalg import solve


def isPD(B):
    try:
        _ = np.linalg.cholesky(B)
        return True
    except np.linalg.LinAlgError:
        return False


def nearestPD(A):
    """Find the nearest positive-definite matrix to input.

    Parameters
    ----------
    A : ndarray
        Any square matrxi, shape (N, N)

    Returns
    -------
    A3 : ndarray
        positive-definite matrix to A

    Notes
    -----
    A Python/Numpy port of John D'Errico's `nearestSPD` MATLAB code [1]_, which
    origins at [2]_.

    References
    ----------
    .. [1] https://www.mathworks.com/matlabcentral/fileexchange/42885-nearestspd
    .. [2] N.J. Higham, "Computing a nearest symmetric positive semidefinite matrix" (1988):
           https://doi.org/10.1016/0024-3795(88)90223-6
    """

    B = (A + A.T) / 2
    _, s, V = np.linalg.svd(B)

    H = np.dot(V.T, np.dot(np.diag(s), V))

    A2 = (B + H) / 2

    A3 = (A2 + A2.T) / 2

    if isPD(A3):
        return A3

    print("Replace current matrix with the nearest positive-definite matrix.")

    spacing = np.spacing(np.linalg.norm(A))

    eye = np.eye(A.shape[0])
    k = 1
    while not isPD(A3):
        mineig = np.min(np.real(np.linalg.eigvals(A3)))
        A3 += eye * (-mineig * k ** 2 + spacing)
        k += 1

    return A3


def robust_pattern(W, Cx, Cs):
    """Transform spatial filters to spatial patterns based on paper [1]_.
        Referring to the method mentioned in article [1],the constructed spatial filter only shows how to combine
        information from different channels to extract signals of interest from EEG signals, but if our goal is
        neurophysiological interpretation or visualization of weights, activation patterns need to be constructed
        from the obtained spatial filters.

    update log:
        2023-12-10 by Leyi Jia <18020095036@163.com>, Add code annotation

    Parameters
    ----------
    W : ndarray
        Spatial filters, shape (n_channels, n_filters).
    Cx : ndarray
        Covariance matrix of eeg data, shape (n_channels, n_channels).
    Cs : ndarray
        Covariance matrix of source data, shape (n_channels, n_channels).

    Returns
    -------
    A : ndarray
        Spatial patterns, shape (n_channels, n_patterns), each column is a spatial pattern.

    References
    ----------
    .. [1] Haufe, Stefan, et al. "On the interpretation of weight vectors of linear models in multivariate neuroimaging.
           Neuroimage 87 (2014): 96-110.
    """
    A = solve(Cs.T, np.dot(Cx, W).T).T
    return A


def xiang_dsp_kernel(X, y):
    """
    DSP: Discriminal Spatial Patterns, only for two classes[1]_.
    Import train data to solve spatial filters with DSP,
    finds a projection matrix that maximize the between-class scatter matrix and
    minimize the within-class scatter matrix. Currently only support for two types of data.

    Author: Swolf <swolfforever@gmail.com>

    Created on: 2021-1-07

    Update log:

    Parameters
    ----------
    X : ndarray
        EEG train data assuming removing mean, shape (n_trials, n_channels, n_samples)
    y : ndarray
        labels of EEG data, shape (n_trials, )

    Returns
    -------
    W : ndarray
        spatial filters, shape (n_channels, n_filters)
    D : ndarray
        eigenvalues in descending order
    M : ndarray
        mean value of all classes and trials, i.e. common mode signals, shape (n_channel, n_samples)
    A : ndarray
        spatial patterns, shape (n_channels, n_filters)

    Notes
    -----
    the implementation removes regularization on within-class scatter matrix Sw.

    References
    ----------
    .. [1] Liao, Xiang, et al. "Combining spatial filters for the classification of single-trial EEG in
        a finger movement task." IEEE Transactions on Biomedical Engineering 54.5 (2007): 821-831.
    """
    X, y = np.copy(X), np.copy(y)
    labels = np.unique(y)
    X = np.reshape(X, (-1, *X.shape[-2:]))
    X = X - np.mean(X, axis=-1, keepdims=True)
    # the number of each label
    n_labels = np.array([np.sum(y == label) for label in labels])
    # average template of all trials
    M = np.mean(X, axis=0)
    # class conditional template
    Ms, Ss = zip(
        *[
            (
                np.mean(X[y == label], axis=0),
                np.sum(
                    np.matmul(X[y == label], np.swapaxes(X[y == label], -1, -2)), axis=0  # Equation (2)
                ),
            )
            for label in labels
        ]
    )
    Ms, Ss = np.stack(Ms), np.stack(Ss)
    # within-class scatter matrix
    Sw = np.sum(
        Ss - n_labels[:, np.newaxis, np.newaxis] * np.matmul(Ms, np.swapaxes(Ms, -1, -2)),
        axis=0,
    )
    Ms = Ms - M
    # between-class scatter matrix
    Sb = np.sum(
        n_labels[:, np.newaxis, np.newaxis] * np.matmul(Ms, np.swapaxes(Ms, -1, -2)),  # Equation (3)
        axis=0,
    )

    D, W = eigh(nearestPD(Sb), nearestPD(Sw))
    ix = np.argsort(D)[::-1]  # in descending order
    D, W = D[ix], W[:, ix]
    A = robust_pattern(W, Sb, W.T @ Sb @ W)

    return W, D, M, A


def xiang_dsp_feature(W, M, X, n_components):
    """
    Return DSP features in paper [1]_.

    Author: Swolf <swolfforever@gmail.com>

    Created on: 2021-1-07

    Update log:

    Parameters
    ----------
    W : ndarray
        spatial filters from csp_kernel, shape (n_channels, n_filters)
    M : ndarray
        common template for all classes, shape (n_channel, n_samples)
    X : ndarray
        eeg test data, shape (n_trials, n_channels, n_samples)
    n_components : int, optional
        length of the spatial filters, first k components to use, by default 1

    Returns
    -------
    features: ndarray
        features, shape (n_trials, n_components, n_samples)

    Raises
    ------
    ValueError
        n_components should less than half of the number of channels

    Notes
    -----
    1. instead of meaning of filtered signals in paper [1]_., we directly return filtered signals.

    References
    ----------
    .. [1] Liao, Xiang, et al. "Combining spatial filters for the classification of single-trial EEG in
        a finger movement task." IEEE Transactions on Biomedical Engineering 54.5 (2007): 821-831.
    """
    W, M, X = np.copy(W), np.copy(M), np.copy(X)
    max_components = W.shape[1]
    if n_components > max_components:
        raise ValueError("n_components should less than the number of channels")
    X = np.reshape(X, (-1, *X.shape[-2:]))
    X = X - np.mean(X, axis=-1, keepdims=True)
    features = np.matmul(W[:, :n_components].T, X - M)
    return features


def proj_ref(Yf):
    '''
    :param Yf: Sin-Cosine reference signals (n_freq, 2 * num_harmonics, n_points)
    :return:
    '''
    Q, R = qr(Yf.T, mode="economic")
    # 计算投影矩阵P
    P = Q @ Q.T  # @ 表示矩阵乘法
    return P


def lagging_aug(X, n_samples, lagging_len, P, training):
    '''
    Parameters
    ----------
    X: Input EEG signals (n_trials, n_channels, n_points)
    n_samples: number of delayed sample points
    lagging_len: lagging length
    P: Projection matrix(n_points, n_points)
    training: True -> training, False -> testing
    Returns: Augmented EEG signals (n_trials, (lagging_len + 1) * n_channels, n_samples)
    -------
    '''
    # Reshape X to (n_trials, n_channels, n_points)
    X = X.reshape((-1, *X.shape[-2:]))
    n_trials, n_channels, n_points = X.shape

    if n_points < lagging_len + n_samples:
        raise ValueError("the length of X should be larger than l+n_samples.")
    aug_X = np.zeros((n_trials, (lagging_len + 1) * n_channels, n_samples))

    if training:
        for i in range(lagging_len + 1):
            aug_X[:, i * n_channels: (i + 1) * n_channels, :] = X[..., i: i + n_samples]
    else:
        for i in range(lagging_len + 1):
            aug_X[:, i * n_channels: (i + 1) * n_channels, : n_samples - i] = X[..., i:n_samples]

    aug_Xp = aug_X @ P
    aug_X = np.concatenate([aug_X, aug_Xp], axis=-1)
    return aug_X


def tdca_feature(X, templates, W, M, Ps, lagging_len, n_components, training=False):
    '''
    参数
    ----------
    X: 输入的EEG信号 (n_trials, n_channels, n_points)
    templates: EEG模板信号 (n_freq, n_channels, n_points)
    W: 空间滤波器 (n_channels, n_filters)
    M: 所有类别的公共模板 (n_channels, n_points)
    Ps: 投影矩阵 (n_freq, n_channels, n_points)
    lagging_len: 延迟长度·
    n_components: 组件数量
    training: True -> 训练, False -> 测试

    返回: 相关系数向量: rhos (n_freq, )
    -------
    '''
    rhos = []
    for Xk, P in zip(templates, Ps):
        a = xiang_dsp_feature(W, M, lagging_aug(X, P.shape[0], lagging_len, P, training=training),
                              n_components=n_components)
        b = Xk[:n_components, :]
        a = np.reshape(a, (-1))
        b = np.reshape(b, (-1))
        rhos.append(pearsonr(a, b)[0])

    print("Index of max rho:", np.argmax(rhos))
    return rhos


class TDCA(BaseEstimator, TransformerMixin, ClassifierMixin):
    def __init__(self, opt, targets):
        self.opt = opt
        self.Fs = opt.Fs
        self.T = int(self.Fs * opt.ws)
        self.Nm = self.opt.Nm
        self.Nc = self.opt.Nc
        self.Nf = self.opt.Nf
        self.dataset = self.opt.dataset
        self.lagging_len = self.opt.lagging_len
        self.n_components = self.opt.n_components
        self.targets = targets

        self.classes_ = np.arange(self.Nf)
        Yf = self.get_Yf(num_harmonics=3, targets=targets)
        self.Ps = [proj_ref(Yf[i]) for i in range(len(self.classes_))]


    def get_Yf(self, num_harmonics, targets):
        '''
        Parameters
        ----------
        num_harmonics: number of harmonics
        targets: stimulus targets
        Returns
        -------
        '''
        Yf = []
        t = np.arange(0, (self.T / self.Fs), step=1.0 / self.Fs)  # 生成时间序列
        for f in targets:
            reference_f = []
            for h in range(1, num_harmonics + 1):
                reference_f.append(np.sin(2 * np.pi * h * f * t)[0:self.T])  # 生成正弦参考信号
                reference_f.append(np.cos(2 * np.pi * h * f * t)[0:self.T])  # 生成余弦参考信号
            Yf.append(reference_f)
        Yf = np.asarray(Yf)  # 转换为numpy数组
        return Yf

    def filter_bank(self, X):
        '''
        Parameters
        ----------
        X: Input EEG signals (n_trials, n_channels, n_points)
        Returns: Output EEG signals of filter banks FB_X (n_fb, n_trials, n_channels, n_points)
        -------
        '''
        FB_X = np.zeros((self.Nm, X.shape[0], self.Nc, X.shape[-1]))  # 初始化滤波器组输出
        nyq = self.Fs / 2  # 计算奈奎斯特频率
        passband = [6, 14, 22, 30, 38, 46, 54, 62, 70, 78]  # 通带频率
        stopband = [4, 10, 16, 24, 32, 40, 48, 56, 64, 72]  # 阻带频率
        highcut_pass, highcut_stop = 80, 90  # 高切频率

        gpass, gstop, Rp = 3, 40, 0.5  # 滤波器参数
        for i in range(self.Nm):
            Wp = [passband[i] / nyq, highcut_pass / nyq]  # 归一化通带频率
            Ws = [stopband[i] / nyq, highcut_stop / nyq]  # 归一化阻带频率
            [N, Wn] = signal.cheb1ord(Wp, Ws, gpass, gstop)  # 计算滤波器阶数和截止频率
            [B, A] = signal.cheby1(N, Rp, Wn, 'bandpass')  # 设计Chebyshev I型滤波器
            data = signal.filtfilt(B, A, X, padlen=3 * (max(len(B), len(A)) - 1)).copy()  # 应用滤波器
            FB_X[i, :, :, :] = data  # 存储滤波后的数据

        return FB_X

    def fit(self, X, y):
        '''
        Parameters
        ----------
        X: Input EEG signals (n_trials, n_channels, n_points)
        y: Input labels (n_trials,)
        Returns
        -------
        '''

        self.W, self.M, self.templates = [], [], []

        self.FB_X_Train = self.filter_bank(X)  # 应用滤波器组
        for fb_i in range(self.Nm):
            X = self.FB_X_Train[fb_i] - np.mean(self.FB_X_Train[fb_i], axis=-1, keepdims=True)  # 去均值
            aug_X_list, aug_Y_list = [], []
            for i, label in enumerate(self.classes_):
                aug_X_list.append(
                    lagging_aug(X[y == label], self.Ps[i].shape[0], self.lagging_len, self.Ps[i], training=True))  # 延迟增强
                aug_Y_list.append(y[y == label])

            aug_X = np.concatenate(aug_X_list, axis=0)  # 合并增强后的数据
            aug_Y = np.concatenate(aug_Y_list, axis=0)

            W_fbi, _, M_fbi, _ = xiang_dsp_kernel(aug_X, aug_Y)  # 计算DSP核
            self.W.append(W_fbi)
            self.M.append(M_fbi)

            self.templates.append(np.stack(
                [np.mean(
                    xiang_dsp_feature(W_fbi, M_fbi, aug_X[aug_Y == label], n_components=W_fbi.shape[1]), axis=0)
                    for label in self.classes_
                ]
            ))
        return self

    def transform(self, X, fb_i):
        '''
        参数
        ----------
        X: 输入的EEG信号 (n_trials, n_channels, n_points)
        返回: rhos (n_trials, n_freq)
        -------
        '''
        X -= np.mean(X, axis=-1, keepdims=True)  # 去均值
        X = X.reshape((-1, *X.shape[-2:]))  # 重塑形状
        rhos = [
            tdca_feature(tmp, self.templates[fb_i], self.W[fb_i], self.M[fb_i], self.Ps, self.lagging_len,
                         n_components=self.n_components)
            for tmp in X
        ]
        rhos = np.stack(rhos)  # 转换为numpy数组
        return rhos

    def predict(self, X, y):
        '''
        Parameters
        ----------
        X: Input EEG signals (n_trials, n_channels, n_points)
        y: Input EEG labels (n_trials, )
        Returns: test_acc (n_trials, )
        -------
        '''

        if self.Nm == 1:
            sum_features = self.transform(X, 0)  # 计算特征

        else:
            sum_features = np.zeros((self.Nm, X.shape[0], self.Nf))  # 初始化特征
            self.FB_X_Test = self.filter_bank(X)  # 应用滤波器组
            for fb_i in range(self.Nm):
                fb_weight = (fb_i + 1) ** (-1.25) + 0.25  # 计算滤波器组权重
                sum_features[fb_i] = fb_weight * self.transform(self.FB_X_Test[fb_i], fb_i)  # 计算加权特征

            sum_features = np.sum(sum_features, axis=0)  # 合并特征

        pred_labels = self.classes_[np.argmax(sum_features, axis=-1)]  # 预测标签
        test_acc = np.mean(y == pred_labels)  # 计算准确率
        return test_acc
