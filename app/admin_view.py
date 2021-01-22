from flask import render_template, flash, redirect, url_for, Blueprint, request
from .models import Option, User, Category, Tag, Post, Comment, Link
from .forms import (
    LoginForm,
    PostForm,
    CategoryForm,
    TagForm,
    CommentForm,
    OptionForm,
    SearchForm,
)
from flask_admin.contrib.sqla import ModelView
from flask_admin import form, helpers, expose

import flask_login as login


class BaseModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # 如果用户没有访问权限， 重定向到登录页面
        return redirect(url_for("auth.login", next=request.url))


class  OptionModelView(BaseModelView):
    pass
    # BaseModelView（）API

class  PageModelView(BaseModelView):
    pass

class  UserModelView(BaseModelView):
    pass

class  CategoryModelView(BaseModelView):
    pass

class  TagModelView(BaseModelView):
    pass

class  PostModelView(BaseModelView):
    pass
    column_exclude_list = ['read_count', 'content_html']

class  CommentModelView(BaseModelView):
    pass

class  LinkModelView(BaseModelView):
    pass





