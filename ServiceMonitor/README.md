# 巡检日志

# 需要工具：
pip install MySQL-python

/* 处理 DOC 格式文件的模块 */
pip install python-docx
http://python-docx.readthedocs.io/en/latest/user/install.html

# 注意
安装时报错：
*********************************************************************************
Could not find function xmlCheckVersion in library libxml2. Is libxml2 installed?
*********************************************************************************
yum -y install libxml2-devel libxslt-devel
pip install lxml

Windows下：
http://xmlsoft.org/sources/win32/python/  需要安装一个 libxml2的库
http://www.microsoft.com/en-us/download/confirmation.aspx?id=44266

pip install wheel
然后去 http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml 下载对应的whl结尾的文件，命令行下跳到当前目录，执行
pip install lxml-3.6.4-cp27-cp27m-win_amd64.whl

下载 http://www.lfd.uci.edu/~gohlke/pythonlibs/#python_docx-0.8.6-py2.py3-none-any.whl
pip install python_docx-0.8.6-py2.py3-none-any.whl

# 安装画图库
pip install numpy
pip install -U pip setuptools
pip install matplotlib



