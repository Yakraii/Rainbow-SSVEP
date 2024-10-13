import eel
import time
import datetime 
# import torch
import csv
import sys
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from brainflow.data_filter import DataFilter
from threading import Thread
# from model import vgg
board = None
board_id = None
brainflow_file_name = ''
def write_file_Openbci_file(data, file_name, channel_number, sampling_rate):
    timeStampFormat = []
    data = data.T
    for item in data[:, 22]:
        time_now = datetime.datetime.fromtimestamp(item)
        time_string = time_now.strftime("%Y-%m-%d %H:%M:%S")
        time_string += str(format(item%1, ".3f"))
        timeStampFormat.append(time_string)
    data_new = np.concatenate((data, np.array([timeStampFormat]).T), axis=1)
    text_create(file_name, channel_number, sampling_rate)
    time.sleep(2)
    file = open(file_name, 'a+')
    np.savetxt(file, data_new, delimiter=',', fmt="%s")
    file.close()
    
def text_create(file_path, channel_number,sample_rate ):
    file = open(file_path, 'w')
    file.write("%OpenBCI Raw EEG Data\n")
    file.write("%Number of channels = "+str(channel_number)+"\n")
    file.write("%Sample Rate = "+str(sample_rate)+" Hz\n")
    file.write("%Board = OpenBCI_GUI$BoardCytonWifi\n")
    str_h = "Sample Index,"
    str_channels = ""
    for i in range(channel_number):
        str_channels += "EXG Channel " + str(i) + ","
    str_other = "Accel Channel 0, Accel Channel 1, Accel Channel 2, Other, Other, Other, Other, Other, Other, Other, Analog Channel 0, Analog Channel 1, Analog Channel 2, Timestamp, Other, Timestamp (Formatted)\n"
    str_channels_header= str_h + str_channels + str_other
    file.write(str_channels_header)
    file.close()

def save_data():
    global board
    global board_id
    dir_path = './data/'
    datafilter = DataFilter()
    data = board.get_board_data()
    time_now = datetime.datetime.now()
    time_string = time_now.strftime("%Y-%m-%d_%H-%M-%S")
    dir_name = dir_path+ "OpenBCISession_" + time_string
    bci_file_name = dir_path + "OpenBCI-RAW-" + time_string+ '.txt'
    brainflow_file_name =dir_path+ "BrainFlow-RAW_"+time_string + '_0' + '.csv'
    datafilter.write_file(data,brainflow_file_name, "w")
    channel_number = len(board.get_eeg_channels(board_id))
    sampling_rate = board.get_sampling_rate(board_id)
    write_file_Openbci_file(data,bci_file_name, channel_number, sampling_rate)

    
def startSession() :
    global board
    global board_id
    board_id = 532
    params = BrainFlowInputParams()
    params.ip_port = 9533
    # params.sampling_rate = "250"
    params.ip_address = '192.168.31.19'
    board = BoardShim(board_id, params)
    board.prepare_session()
 
@eel.expose
def start():
    global board
    global brainflow_file_name
    dir_path = './data/'
    time_now = datetime.datetime.now()
    time_string = time_now.strftime("%Y-%m-%d_%H-%M-%S")
    brainflow_file_name =dir_path+ "BrainFlow-RAW_"+time_string + '_0' + '.csv'
    # board.start_stream(45000, 'file://'+brainflow_file_name+':w')


@eel.expose
def stop():
    global board
    # board.stop_stream()
    # board.release_all_sessions()
    time.sleep(2)
    sys.exit(0)


@eel.expose
def trigger(marker):
    global board
    # board.insert_marker(marker+1)
    return 1


def main():
    # startSession()
    eel.init('web')
    eel.start("index.html")
    

if __name__ == '__main__':
    main()