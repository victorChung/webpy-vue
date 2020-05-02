#进入server目录
python -m venv venv

------------------------------------
#linux or os X
. venv/bin/activate
#退出venv环境
deactivate

#windows
.\venv\Script\activate
#退出venv环境
.\venv\Scripts\deactivate.bat


------------------------------------
#安装依赖包
pip install web.py xlrd xlwt

------------------------------------
#启动
python app.py

