# Flask Voice Recognition Project

## 项目概述
这个项目是一个基于 Flask 的语音识别和回复系统，使用百度的语音识别 API 来实现语音到文本的转换，并根据关键词生成相应的回复。该项目还提供了相关的测试功能，确保各个模块的正确性。

asr_raw.py是官方给出的测试demo
## 安装依赖
确保已安装 Python 3.x，然后在项目根目录下运行以下命令来创建虚拟环境并安装依赖：

```bash
# 创建虚拟环境
python -m venv venv_library_root

# 激活虚拟环境
# Windows
venv_library_root\Scripts\activate
# macOS/Linux
source venv_library_root/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 使用说明
配置 API 密钥： 在 config.py 中，替换 API_KEY 和 SECRET_KEY 为你自己的百度 API 密钥。

启动 Flask 应用： 在根目录下启动 Flask 应用：python app.py

```bash
# 复制代码
python app.py
```
然后在浏览器中访问 http://127.0.0.1:5000。

使用音频文件： 将音频文件放在 static 目录下，应用将会处理这些文件并返回相应的文本和回复。

## 测试
替换test_utils.py中的wav相关文件与对应的路径信息
然后运行 test_utils.py
```aiignore
python -m unittest tests.test_utils

```