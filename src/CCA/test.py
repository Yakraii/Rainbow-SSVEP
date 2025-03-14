import argparse

print('halo')

if __name__ == '__main__':
    # 接收两个个参数：csv文件地址、频率1
    parser = argparse.ArgumentParser(description="Data processing script.")
    parser.add_argument('--file_path', type=str, default="", help='Path to the raw CSV file')
    parser.add_argument('--frequencies', type=float, nargs='*', default=[7, 8, 11, 12], help='List of frequencies')
    
    args = parser.parse_args()
    print("halo")
    print("File path:", args.file_path)
    print("Frequencies:", args.frequencies)