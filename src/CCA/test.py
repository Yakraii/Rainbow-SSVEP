import pandas as pd
from pathlib import Path

# 目标频率与新标记的映射
TARGET_FREQS = {
    7.5: 1,
    9.75: 2,
    10.25: 3,
    12.25: 4,
    14.25: 5
}


def process_file(file_path, result_df):
    """处理单个CSV文件"""
    # 解析文件名获取频率
    file_name = Path(file_path).stem
    freq1, freq2 = map(float, file_name.split('&'))

    df = pd.read_csv(file_path)

    # 处理两个频率对应的数据段
    for orig_marker, freq in [(1, freq1), (2, freq2)]:
        if freq not in TARGET_FREQS:
            continue

        # 获取新标记
        new_marker = TARGET_FREQS[freq]

        # 找到标记开始和结束的位置
        markers = df[df['marker'] == orig_marker].index.tolist()
        if len(markers) != 2:
            print(f"文件 {file_path} 中标记 {orig_marker} 出现次数不为2，已跳过")
            continue

        start, end = markers[0], markers[1]

        # 提取有效数据（不包含标记行）
        segment = df.iloc[start: end + 1].copy()
        # segment['marker'] = new_marker

        result_df.append(segment)


def main(input_files, output_file):
    """主函数"""
    all_data = []

    for file in input_files:
        process_file(file, all_data)

    if not all_data:
        print("未找到有效数据")
        return

    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv(output_file, index=False)
    print(f"结果已保存至 {output_file}")


if __name__ == "__main__":
    # 输入文件列表（请替换为实际路径）
    input_files = [
        '../../data/7.5&10.csv',
        '../../data/9.75&14.25.csv',
        '../../data/12.25&10.25.csv'
    ]

    # 输出文件路径
    output_file = '../../data/merged_data.csv'

    main(input_files, output_file)