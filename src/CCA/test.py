import pandas as pd  # 导入pandas库，用于数据处理
from pathlib import Path  # 导入Path类，用于处理文件路径

# 定义目标频率与标记的映射关系
TARGET_FREQS = {
    7.5: 1,
    9.75: 2,
    10.25: 3,
    12.25: 4,
    14.25: 5
}

# 定义处理文件的函数
def process_file(file_path, result_df):
    file_name = Path(file_path).stem  # 获取文件名（不包括扩展名）
    try:
        freq1, freq2 = map(float, file_name.split('&'))  # 从文件名中提取两个频率值
    except ValueError:
        print(f"文件名 {file_name} 格式不正确")  # 如果文件名格式不正确，打印错误信息
        return

    df = pd.read_csv(file_path)  # 读取CSV文件
    df['marker'] = df['marker'].astype(int)  # 将'marker'列转换为整数类型

    df_modified = df.copy()  # 创建数据副本

    # 遍历原始标记和频率的对应关系
    for orig_marker, freq in [(1, freq1), (2, freq2)]:
        if freq not in TARGET_FREQS:  # 如果频率不在目标频率中，跳过
            continue

        new_marker = TARGET_FREQS[freq]  # 获取新的标记值

        markers = df[df['marker'] == orig_marker].index.tolist()  # 获取原始标记的索引列表
        if len(markers) != 2:
            print(f"文件 {file_path} 中标记 {orig_marker} 出现次数不为2，已跳过")  # 如果标记出现次数不为2，打印错误信息
            continue

        start, end = markers[0], markers[1]  # 获取标记的起始和结束索引

        df_modified.at[start, 'marker'] = new_marker  # 修改起始索引处的标记值
        df_modified.at[end, 'marker'] = new_marker  # 修改结束索引处的标记值

        segment = df_modified.iloc[start:end + 1].copy()  # 提取标记之间的片段
        result_df.append(segment)  # 将片段添加到结果列表中

# 定义主函数
def main(input_files, output_file):
    all_data = []  # 创建空列表用于存储所有数据

    for file in input_files:  # 遍历输入文件列表
        process_file(file, all_data)  # 处理每个文件

    if not all_data:  # 如果没有有效数据
        print("未找到有效数据")  # 打印提示信息
        return

    final_df = pd.concat(all_data, ignore_index=True)  # 合并所有数据
    final_df.to_csv(output_file, index=False)  # 将合并后的数据保存为CSV文件
    print(f"合并完成，保存至：{output_file}")  # 打印保存成功信息

# 主程序入口
if __name__ == "__main__":
    input_files = [  # 定义输入文件列表
        '../../data/data_raw/7.5&10.csv',
        '../../data/data_raw/9.75&14.25.csv',
        '../../data/data_raw/12.25&10.25.csv'
    ]
    output_file = '../../data/merged.csv'  # 定义输出文件路径

    main(input_files, output_file)  # 调用主函数