import argparse
from pprint import pprint
import os
import pandas as pd

def main(data_path):
    # root_path = getPath.getRootPath()
    # data_path = os.path.join(root_path, 'data', 'data.csv')
    # 读取csv
    df = pd.read_csv(data_path)
    # 统计 marker 列，剔除 0 并打印每个数字及其出现的次数
    pprint(df[df['marker'] != 0]['marker'].value_counts())

    print()
    #  打印marker列不为0的行
    pprint(df[df['marker'] != 0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='CSV 文件的路径', required=True)   # 添加一个参数，用于指定 CSV 文件的路径
    args = parser.parse_args()    # 解析命令行参数
    main(args.file)
