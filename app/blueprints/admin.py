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
from ..extensions import db
from ..forms import (
    LoginForm,
    PostForm,
    CategoryForm,
    TagForm,
    CommentForm,
    OptionForm,
    SearchForm,
)


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
def index():
    pagination = Post.query.order_by(Post.created.desc()).paginate(per_page=10)
    return render_template(
        "admin/index.html", posts=pagination.items, pagination=pagination
    )


@admin_bp.route("/admin/write_post", methods=["GET", "POST"])
def write_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, content=content, category=category)
        # same with:
        # category_id = form.category.data
        # post = Post(title=title, body=body, category_id=category_id)
        db.session.add(post)
        db.session.commit()
        flash("文章已发布", "success")
        return redirect(url_for("main.post", post_id=post.id))
    return render_template("admin/write_post.html", form=form)


@admin_bp.route("/admin/option", methods=["GET", "POST"])
def option():
    form = OptionForm()
    blog_title = Option.query.filter_by(name="blog_title").first()
    blog_sub_title = Option.query.filter_by(name="blog_sub_title").first()
    blog_about = Option.query.filter_by(name="blog_about").first()
    blog_footer = Option.query.filter_by(name="blog_footer").first()
    
    if form.validate_on_submit():    
        blog_title.value = form.blog_title.data  
        blog_sub_title.value = form.blog_sub_title.data
        blog_about.value = form.blog_about.data
        blog_footer.value = form.blog_footer.data

        db.session.commit()
        flash("设置保存成功", "success")
        return redirect(url_for("main.index"))
    form.blog_title.data = blog_title.value
    form.blog_sub_title.data = blog_sub_title.value
    form.blog_about.data = blog_about.value
    form.blog_footer.data = blog_footer.value
    return render_template("admin/option.html", form=form)


@admin_bp.route("/admin/manage_categories")
def manage_categories():
    pass
    return render_template("admin/manage_categories.html")


@admin_bp.route("/admin/manage_tags")
def manage_tags():
    pass
    return render_template("admin/manage_tags.html")


@admin_bp.route("/admin/manage_posts")
def manage_posts():
    pass
    return render_template("admin/manage_posts.html")


@admin_bp.route("/admin/manage_comments")
def manage_comments():
    pass
    return render_template("admin/manage_comments.html")


@admin_bp.route("/admin/manage_links")
def manage_links():
    pass
    return render_template("admin/manage_links.html")