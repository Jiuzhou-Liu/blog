from flask import (
    current_app,
    flash,
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    make_response,
)
from ..models import Option, User, Category, Tag, Post, Comment, Link
from ..forms import LoginForm, PostForm, CategoryForm, TagForm, CommentForm, OptionForm, SearchForm
from ..extensions import db
from sqlalchemy import extract, and_, or_

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    pagination = Post.query.order_by(Post.created.desc()).paginate(per_page=10)
    return render_template(
        "main/index.html", posts=pagination.items, pagination=pagination
    )


@main_bp.route("/about")
def about():
    return render_template("main/about.html")


@main_bp.route("/category/<int:category_id>")
def category(category_id):
    category = Category.query.get_or_404(category_id)
    pagination = (
        Post.query.with_parent(category)
        .order_by(Post.created.desc())
        .paginate(per_page=10)
    )
    return render_template(
        "main/archive.html",
        type="分类",
        archive=category,
        posts=pagination.items,
        pagination=pagination,
    )


@main_bp.route("/tag/<int:tag_id>")
def tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    pagination = (
        Post.query.with_parent(tag).order_by(Post.created.desc()).paginate(per_page=10)
    )
    return render_template(
        "main/archive.html",
        type="标签",
        archive=tag,
        posts=pagination.items,
        pagination=pagination,
    )


@main_bp.route("/archive/<int:archive_year>/<int:archive_month>")
def archive(archive_year, archive_month):
    pagination = Post.query.filter(
        and_(
            extract("year", Post.created) == archive_year,
            extract("month", Post.created) == archive_month,
        )
    ).paginate(per_page=10)
    archive = {
        "name": str(archive_year) + "年" + str(archive_month) + "月",
        "posts": pagination.items,
    }
    return render_template(
        "main/archive.html",
        type="归档",
        archive=archive,
        posts=archive["posts"],
        pagination=pagination,
    )


@main_bp.route("/search/<string:keyword>", methods=["GET", "POST"])
def search(keyword):
    keyword = request.args.get("keyword")
    pagination = Post.query.filter(
        or_(
            Post.content.like("%" + keyword + "%"), Post.title.like("%" + keyword + "%")
        )
    ).paginate(per_page=10)
    archive = {"name": keyword, "posts": pagination.items}
    return render_template(
        "main/archive.html",
        type="搜索",
        archive=archive,
        posts=archive["posts"],
        pagination=pagination,
    )


@main_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    post.read_count = post.read_count + 1
    db.session.commit()
    pagination = (
        Comment.query.with_parent(post)
        .filter_by(reviewed=True)
        .order_by(Comment.created.desc())
        .paginate(per_page=10)
    )
    return render_template(
        "main/post.html",
        post=post,
        post_comments=pagination.items,
        pagination=pagination,
    )
