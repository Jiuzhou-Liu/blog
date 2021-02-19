from .models import Option, Page, User, Category, Tag, Post, Comment, Link

from flask_wtf import FlaskForm
from wtforms import (
    ValidationError,
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    TextAreaField,
    SelectMultipleField,
    HiddenField,
)
from wtforms.validators import DataRequired, Email, URL, Optional
from flask import request


class LoginForm(FlaskForm):
    name = StringField("名字", validators=[DataRequired()], render_kw={"class": ""})
    password = PasswordField("密码", validators=[DataRequired()])
    remember = BooleanField("记住我")
    submit = SubmitField("登录")


class PostForm(FlaskForm):
    title = StringField("标题", validators=[DataRequired()])
    category = SelectField("分类", coerce=int, default=1)
    tags = SelectMultipleField("标签", coerce=int)
    content = TextAreaField("内容", validators=[DataRequired()])
    submit = SubmitField("发布文章")

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [
            (category.id, category.name)
            for category in Category.query.order_by(Category.name).all()
        ]
        self.tags.choices = [
            (tag.id, tag.name) for tag in Tag.query.order_by(Tag.name).all()
        ]


class PageForm(FlaskForm):
    title = StringField("标题", validators=[DataRequired()])
    slug = StringField("英文标识", validators=[DataRequired()])
    content = TextAreaField("内容", validators=[DataRequired()])
    submit = SubmitField("提交")


class CategoryForm(FlaskForm):
    name = StringField("名称", validators=[DataRequired()])
    submit = SubmitField("提交")

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError("分类名称已存在")


class TagForm(FlaskForm):
    name = StringField("名称", validators=[DataRequired()])
    submit = SubmitField("提交")

    def validate_name(self, field):
        if Tag.query.filter_by(name=field.data).first():
            raise ValidationError("标签名称已存在")


class CommentForm(FlaskForm):
    author = StringField("名字", validators=[DataRequired()])
    mail = StringField("邮箱", validators=[DataRequired()])
    url = StringField(
        "网站", validators=[Optional(), URL()], render_kw={"placeholder": "http://"}
    )
    content = TextAreaField(
        "内容", validators=[DataRequired()], render_kw={"placeholder": "请勿发表垃圾评论"}
    )
    submit = SubmitField("提交")

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.author.render_kw = {"value": request.cookies.get("remember_author", "")}
        self.mail.render_kw = {"value": request.cookies.get("remember_mail", "")}
        self.url.render_kw = {"value": request.cookies.get("remember_url", "")}


class LoginCommentForm(CommentForm):
    author = HiddenField()
    mail = HiddenField()
    url = HiddenField()

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.author.render_kw = {"value": User.query.first().name}
        self.mail.render_kw = {"value": User.query.first().mail}
        self.url.render_kw = {"value": ""}


class LinkForm(FlaskForm):
    name = StringField("名称", validators=[DataRequired()])
    url = StringField("地址", validators=[Optional(), URL()])
    submit = SubmitField("提交")


class OptionForm(FlaskForm):
    blog_title = StringField("标题", validators=[DataRequired()])
    blog_sub_title = StringField("子标题")
    blog_navbar = TextAreaField("导航栏右侧")
    blog_footer = TextAreaField("页脚")
    sidebar_comment = BooleanField("侧边栏-近期评论")
    comment_review = BooleanField("评论需要审核")
    submit = SubmitField("保存设置")


class SearchForm(FlaskForm):
    keyword = StringField("关键字", validators=[DataRequired()])
    submit = SubmitField()
