import numpy as np 
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations
from scipy import signal
from matplotlib import pyplot as plt
import scipy
import os 
files = os.listdir('./data1')
for file in files:
    data = np.loadtxt('./data1/'+ file).T

    indexs = data[-12]
    print(indexs)
    for id in range(len(indexs)-1):
        if indexs[id+1] - indexs[id] != 1:
            print('==================', id, indexs[id+1] - indexs[id])
        