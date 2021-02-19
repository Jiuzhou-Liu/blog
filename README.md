# Onelog

*一个基于 Flask 的极简主义博客程序*  

功能列表:  
页面、分类、标签、归档、文章、搜索、随机查看文章、上一篇下一篇、评论、链接、后台

登录后台:   
<http://127.0.0.1:5000/auth/login>  
用户名: admin  
密码: 123456

## 安装

克隆代码:
```
$ git clone https://github.com/liujiuzhou/onelog.git
$ cd onelog
```
安装 Pipenv:
```
$ pip install pipenv
```
使用 Pipenv 创建并激活虚拟环境然后安装依赖项:
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
