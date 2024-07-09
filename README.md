# CosmosRP-8k的客户端,包括做成可执行文件


## 直接运行
- pip install -r requirements.txt
- python app.py

## 编译成exe或linux可执行文件
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt
- pip install pyinstaller 
- pyinstaller app.spec
- 编译好的在dist目录里面

#这个app.spec也可以做其他的gradio单文件可执行文件哦:)