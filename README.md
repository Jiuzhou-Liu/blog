# Onelog

*一个基于 Flask 的极简主义博客程序*  

演示: <http://3ghh.cn>

## 安装

clone:
```
$ git clone https://github.com/pythoneer/onelog.git
$ cd onelog
```
创建并激活虚拟环境然后安装依赖项: 

使用 venv/virtualenv + pip:
```
$ py -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
或者使用 Pipenv:
```
$ pipenv install --dev
$ pipenv shell
```
生成虚拟数据然后运行:
```
$ flask forge
$ flask run
* Running on http://127.0.0.1:5000/
```
