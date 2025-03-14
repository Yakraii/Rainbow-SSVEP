import pandas as pd
import tkinter as tk
from tkinter import filedialog

# 写一个选择csv文件的ui界面，然后读取csv文件，然后进行数据处理，最后输出数据的形状
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    return file_path

def read_csv(file_path):
    data = pd.read_csv(file_path)
    return data

def process_data(data):
    # Add your data processing code here
    processed_data = data  # Placeholder for actual processing
    return processed_data

def main():
    file_path = select_file()
    if file_path:
        data = read_csv(file_path)
        processed_data = process_data(data)
        print("Data shape:", processed_data.shape)

if __name__ == "__main__":
    main()