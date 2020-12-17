from .models import Option, User, Category, Tag, Post, Comment, Link

from flask_wtf import FlaskForm
from wtforms import (
    ValidationError,
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, URL, Optional


class LoginForm(FlaskForm):
    name = StringField("名字", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    remember = BooleanField("记住我")
    submit = SubmitField("登录")


class PostForm(FlaskForm):
    title = StringField("标题", validators=[DataRequired()])
    category = SelectField("分类", coerce=int, default=1)
    content = TextAreaField("内容", validators=[DataRequired()])
    submit = SubmitField("发布文章")

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [
            (category.id, category.name)
            for category in Category.query.order_by(Category.name).all()
        ]


class CategoryForm(FlaskForm):
    name = StringField("名称", validators=[DataRequired()])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError("分类名称已存在")


class TagForm(FlaskForm):
    name = StringField("名称", validators=[DataRequired()])
    submit = SubmitField()

    def validate_name(self, field):
        if Tag.query.filter_by(name=field.data).first():
            raise ValidationError("标签名称已存在")


class CommentForm(FlaskForm):
    author = StringField("名字", validators=[DataRequired()])
    mail = StringField("邮箱", validators=[DataRequired()])
    url = StringField("网站", validators=[Optional(), URL()])
    content = TextAreaField("内容", validators=[DataRequired()])
    submit = SubmitField()


class OptionForm(FlaskForm):
    blog_title = StringField("标题", validators=[DataRequired()])
    blog_sub_title = StringField("子标题")
    blog_about = TextAreaField("关于页面")
    blog_footer = TextAreaField("页脚")
    submit = SubmitField("保存设置")


class SearchForm(FlaskForm):
    keyword = StringField("关键字", validators=[DataRequired()])
    submit = SubmitField()
