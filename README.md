## 程序启动
- 在Windows系统中，使用以下命令：
```shell
venv\Scripts\activate.bat
```

- 在Mac或Linux系统中，使用以下命令：
```shell
source venv/bin/activate
```
## 安装
- 关于导出包，如果您想要导出您已安装的包列表，可以使用以下命令：
```shell
pip freeze > requirements.txt
```
- 安装包： 在venv环境激活后，您可以使用以下命令来安装requirements.txt中列出的所有包：
```shell
pip install -r requirements.txt
```


- 验证安装： 安装完成后，您可以运行以下命令来验证安装的包列表：
```shell
pip list
```

这将列出venv环境中已安装的所有包。

- 安装环境
```shell
apt install python3-venv

python.exe -m pip install --upgrade pip
```

## 基础的图形界面

```shell
pip install tk 
pip install pyinstaller

pyinstaller -w -F main.py
```


