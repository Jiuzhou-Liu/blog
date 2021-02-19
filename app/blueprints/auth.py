from flask import render_template, flash, redirect, url_for, Blueprint
from ..models import Option, Page, User, Category, Tag, Post, Comment, Link
from ..forms import LoginForm, PostForm, PageForm, CategoryForm, TagForm, CommentForm, OptionForm, SearchForm

from flask_login import login_user, logout_user, login_required, current_user
from ..utils import redirect_back

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.first()
        if user:
            if name == user.name and user.validate_password(password):
                login_user(user, remember)
                flash("欢迎回来", "info")
                return redirect_back()
            flash("用户名或密码无效", "warning")
        else:
            flash("用户名不存在", "warning")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("注销成功", "info")
    return redirect_back()