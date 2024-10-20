from pathlib import Path

def getRootPath():
    # 获取当前文件的绝对路径
    current_file = Path(__file__).resolve()
    # 逐级向上查找，直到找到包含 README.md 的目录
    project_root = current_file
    while not (project_root / 'root/').exists() and project_root != project_root.parent:
        project_root = project_root.parent
    # print("Module/getPath.py: Find root:", project_root)
    return project_root
