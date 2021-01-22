from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_wtf import CSRFProtect
from flask_moment import Moment

from flask_admin import Admin, AdminIndexView, expose
from flask import flash, redirect, url_for, request

db = SQLAlchemy()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if current_user.is_authenticated:
            return super(MyAdminIndexView, self).index()
        flash("没有权限访问该页面!")
        return redirect(url_for("auth.login", next=request.url))


admin = Admin()
admin.name = "Onelog管理后台"
admin.template_mode = "bootstrap4"
admin.index_view = MyAdminIndexView()
admin.base_template = "admin/base.html"


@login_manager.user_loader
def load_user(user_id):
    from .models import User

    user = User.query.get(int(user_id))
    return user


login_manager.login_view = "auth.login"
login_manager.login_message = "请先登录"
login_manager.login_message_category = "warning"
