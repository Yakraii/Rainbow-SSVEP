# Rainbow-SSVEP

## 项目简介
🌈Rainbow-SSVEP 是一个研究稳态视觉诱发电位 (SSVEP) 的项目。

## 目录
- [安装](#安装)
- [使用方法](#使用方法)
- [贡献](#贡献)
- [许可证](#许可证)

## 注意事项
部分 Python 包 (例如brainflow) 需要使用我们提供的版本。
请确保在 `PYTHONPATH` 中添加 `src` 目录。你可以在 `.pth` 文件中添加以下内容：

```text
/path/to/Rainbow-SSVEP/src
```

## 安装
请按照以下步骤进行安装：

1. 克隆仓库：
    ```bash
    git clone https://github.com/yourusername/Rainbow-SSVEP.git
    ```
2. 进入项目目录：
    ```bash
    cd Rainbow-SSVEP
    ```
3. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
4. 安装前端
    ```bash
    cd SSVEP-WDBE
    npm install
    ```


## 使用方法
运行以下命令以启动项目：
```bash
npm run dev
python app.py
```

## 贡献
欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

## 许可证
...