# Rainbow-SSVEP
![Version](https://img.shields.io/badge/version-0.9.2-blue)  ![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&color=3776AB&labelColor=FFD43B) ![License](https://img.shields.io/badge/license-Apache%202.0-green)      ![Contributors](https://img.shields.io/github/contributors/Yakraii/Rainbow-SSVEP) ![Stars](https://img.shields.io/github/stars/Yakraii/Rainbow-SSVEP)

## 项目简介
🌈Rainbow-SSVEP 是一个研究稳态视觉诱发电位 (SSVEP) 的项目。

## 目录
- [安装](#安装)
- [使用方法](#使用方法)
- [贡献](#-贡献)
- [联系](#-联系我们)
- [许可证](#-许可证)

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
**注意**：请在启动项目之前，根据脑电帽的参数配置好 `config/config.yaml` 文件。


## 📬 联系我们 
如果您有任何问题或建议，欢迎通过以下方式联系我：  
- **GitHub Issues**：在 [Issues](https://github.com/your-username/your-repo/issues)  中提出你的问题。  
- **Email**：发送邮件至 [yakraii@163.com](mailto:yakraii@163.com) ，我会尽快回复。

## 🤝 贡献
欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

## 📝 许可证
本项目采用 Apache  2.0。

## 📚 引用
[1] [Canonical_Classifier By YuDongPan](https://github.com/YuDongPan/Canonical_Classifier)
[2] Nakanishi M, Wang YT, Jung TP, et al. Detecting Glaucoma With a Portable Brain-Computer Interface for Objective Assessment of Visual Function Loss. 
https://jamanetwork.com/journals/jamaophthalmology/fullarticle/2621879