# Onelog

*一个基于 Flask 的极简主义博客程序*  

功能列表:  
页面、分类、标签、归档、文章、搜索、随机查看文章、上一篇下一篇、评论、链接、后台

下一步开发计划:  
1. 回复评论时直接在目标评论下方显示输入框
2. 使用 flask-admin 扩展重构后台管理
3. 插件功能实现
4. 设计icon
5. 界面优化仿简书


演示: 
<http://3ghh.cn>

## 安装

克隆代码:
```
$ git clone https://github.com/pythoneer/onelog.git
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
