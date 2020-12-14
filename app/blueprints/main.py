from flask import Blueprint, render_template, request, current_app
from ..models import Post, Category, Tag

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.order_by(
        Post.created.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('main/index.html', pagination=pagination, posts=posts)


@main_bp.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('main/about.html')


@main_bp.route('/category/<int:category_id>', methods=['GET', 'POST'])
def category(category_id):
    category = Category.query.get_or_404(category_id)
    page = 1

    pagination = Post.query.with_parent(category).order_by(
        Post.created.desc()).paginate(page, 10)
    posts = pagination.items
    return render_template('main/archive.html', type="分类", archive=category, pagination=pagination, posts=posts)


@main_bp.route('/tag/<int:tag_id>', methods=['GET', 'POST'])
def tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    page = 1

    pagination = Post.query.with_parent(tag).order_by(
        Post.created.desc()).paginate(page, 10)
    posts = pagination.items
    return render_template('main/archive.html', type="标签", archive=tag, pagination=pagination, posts=posts)

@main_bp.route('/archive/<int:archive_id>', methods=['GET', 'POST'])
def archive(archive_id):
    archive = Tag.query.get_or_404(archive_id)
    page = 1

    pagination = Post.query.with_parent(archive_id).order_by(
        Post.created.desc()).paginate(page, 10)
    posts = pagination.items
    return render_template('main/archive.html', type="归档", archive=archive, pagination=pagination, posts=posts)


@main_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('main/post.html',  post=post)


""" 






























class LoginFrom(FlaskForm):
    username = StringField('Username', validators=[DataRequired(
    )], default='2267719005', render_kw={'class': 'name'})
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(1, 10)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


@bp.route('/a', methods=['GET', 'POST'])
def index():
    users = {
        'username': 'Grey Li',
        'bio': 'A boy who loves movies and music.',
    }

    movies = [
        {'name': 'tom', 'age': 13},
        {'name': 'jack', 'age': -18},
        {'name': '555', 'age': 0}
    ]

    # 发一条所有模板可以调用的闪现消息
    # flash("哈哈哈哈哈哈")

    # 输出表单代码
    form = LoginFrom()

    if form.validate_on_submit():
        # return request.form['username']
        return form.username.data
    else:
        return render_template('blog/index.html', form=form, users=users, movies=movies)
 """
