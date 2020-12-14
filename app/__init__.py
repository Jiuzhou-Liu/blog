import os
from flask import Flask
from .settings import config
from .extensions import db, toolbar
from .blueprints import main, auth
from .models import Option, User, Category, Tag, Post, Comment, Link
from sqlalchemy.sql.expression import func
from sqlalchemy import extract
import click


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    # 初始化应用
    app = Flask(__name__)

    # 导入配置文件
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    toolbar.init_app(app)

    # 注册蓝图
    app.register_blueprint(main.main_bp)
    app.register_blueprint(auth.auth_bp)

    # 创建模板上下文
    @app.context_processor
    def make_template_context():
        options = {}
        for option in Option.query.all():
            options[option.name] = option.value

        categorys = Category.query.all()

        tags = Tag.query.order_by(Tag.name).all()

        comments = Comment.query.order_by(Comment.author).all()

        links = Link.query.order_by(Link.name).all()

        archives = db.session.query(extract('month', Post.created).label('month'), extract(
            'year', Post.created).label('year'), func.count('*').label('count')).group_by('month').all()

        return dict(options=options, categorys=categorys, tags=tags, archives=archives, comments=comments, links=links)

    # 创建Shell命令
    @ app.cli.command()
    @ click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """创建数据库
        """
        if drop:
            click.confirm(
                'This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @ app.cli.command()
    def forge():
        """生成虚拟数据
        """
        from .fakes import fake_option, fake_user, fake_categorys, fake_tags, fake_posts, fake_comments, fake_links
        db.drop_all()
        db.create_all()

        click.echo('Generating blog information')
        fake_option()

        click.echo('Generating the administrator...')
        fake_user()

        click.echo('Generating categorys...')
        fake_categorys()

        click.echo('Generating tags...')
        fake_tags()

        click.echo('Generating posts...')
        fake_posts()

        click.echo('Generating comments...')
        fake_comments()

        click.echo('Generating links...')
        fake_links()

        click.echo('Done.')

    return app


'''
























































'''


def create_app2(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)

    # 导入配置对象
    from .settings import config
    app.config.from_object(config[config_name])

    # 路由
    @ app.route('/')
    # 视图函数
    def index():
        return 'hello world!'

    '''

    # 注册一个函数可以在渲染任意模板时传入模板全局对象
    @app.context_processor
    def f1():
        # 调用任意render_template()时 将数据传入模板
        return dict(v1="3")
    '''
    # lambda 简化上个示例
    app.context_processor(lambda: dict(v1='5'))

    '''
    # 注册一个模板过滤器
    @app.template_filter()
    def add_one(s):
        return int(s)+1
    '''

    # 注册一个模板中的测试器
    @ app.template_test()
    def dayu5(s):
        return int(s) > 5

    # 注册错误处理函数
    @ app.errorhandler(404)
    def not_found(e):
        return '', 404

    # 每个函数请求前执行

    @ app.before_request
    def do_something():
        # 获取url参数保存到即刻定义的全局变量
        g.name = request.args.get("name", "Tom")

    @ app.route('/404')
    def not_found():
        # 主动引发404异常
        abort(404)

    @ app.route('/a')
    # 重定向回上一个页面
    def redirect_back():
        # url_for 参数必须是定义了路由的视图函数
        return redirect(request.referrer or url_for('.not_found'))

    # 返回json或其他类型数据或自定义响应头部
    @ app.route('/json')
    def json():
        # 方法1
        obj = {
            'name': 'liujiuzhou'
        }
        return jsonify(obj)

        # 方法2
        content = """{
    "data": {
        "name": "liujiuzhou"
    }
}"""
        heder = {
            "Content-Type": "application/json",
            "Set-Cookie": "user_lang=language111; Path=/"
        }
        return content, "200", heder

        # 方法3: 手动创建响应
        response = make_response(content)
        response.mimetype = "application/json"
        response.set_cookie('user_lang', 'language111')
        return response

    @app.route('/post')
    @app.route('/post/<string:crud>/', methods=['GET', 'POST'])
    def edit(crud='edit'):
        # 对指定的帖子进行四种操作操作 增查改删 create/read/update/delete/
        session.pop('te1st')
        session['te1st'] = True
        if 'te1st' not in session:
            abort(403)
        if request.method == 'POST':
            pass
        else:
            # return request.cookies.get('user_l1ang', 'default')
            #  return redirect(url_for('not_found'), "302")  # 默认301临时重定向
            id = request.args.get('id', '1')
            res = '你正在' + crud + '-id为' + id + '的帖子'

            # 在此视图结束后执行
            @after_this_request
            def do_something2(response):
                pass
                response.set_cookie('user_lang', 'language111')
                return response

            return res, 200, {"Set-Cookie": "user_lang=language111; Path=/", 'Content-Type': 'text/html; charset=utf-8'}

    @app.cli.command()
    def init_db():
        # 命令说明
        click.echo("初始化数据库中")

    from .blueprints import blog
    app.register_blueprint(blog.bp)

    return app
