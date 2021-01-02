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
    LinkForm,
    SearchForm,
)

from flask_login import login_required, current_user

from ..utils import redirect_back

admin_bp = Blueprint("admin", __name__)


@admin_bp.before_request
@login_required
def login_protect():
    pass


@admin_bp.route("/option", methods=["GET", "POST"])
def option():
    form = OptionForm()
    blog_title = Option.query.filter_by(name="blog_title").first()
    blog_sub_title = Option.query.filter_by(name="blog_sub_title").first()
    blog_about = Option.query.filter_by(name="blog_about").first()
    blog_footer = Option.query.filter_by(name="blog_footer").first()
    sidebar_comment = Option.query.filter_by(name="sidebar_comment").first()
    comment_review = Option.query.filter_by(name="comment_review").first()

    if form.validate_on_submit():
        blog_title.value = form.blog_title.data
        blog_sub_title.value = form.blog_sub_title.data
        blog_about.value = form.blog_about.data
        blog_footer.value = form.blog_footer.data
        sidebar_comment.value = form.sidebar_comment.data
        comment_review.value = form.comment_review.data

        db.session.commit()
        flash("设置保存成功", "success")
        return redirect(url_for("main.index"))
    form.blog_title.data = blog_title.value
    form.blog_sub_title.data = blog_sub_title.value
    form.blog_about.data = blog_about.value
    form.blog_footer.data = blog_footer.value
    form.sidebar_comment.data = int(sidebar_comment.value)
    form.comment_review.data = int(comment_review.value)

    return render_template("admin/option.html", form=form)


@admin_bp.route("/manage_categories")
def manage_categories():
    categories = Category.query.all()
    return render_template("admin/manage_categories.html", categories=categories)


@admin_bp.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash("编辑成功", "success")
        return redirect(url_for("admin.manage_categories"))
    form.name.data = category.name
    return render_template("admin/category.html", form=form, type="编辑")


@admin_bp.route("/add_category", methods=["GET", "POST"])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash("添加成功", "success")
        return redirect(url_for("admin.manage_categories"))
    return render_template("admin/category.html", form=form, type="添加")


@admin_bp.route("/category/<int:category_id>/delete", methods=["POST"])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("删除成功", "success")
    return redirect_back()


@admin_bp.route("/manage_tags")
def manage_tags():
    tags = Tag.query.all()
    return render_template("admin/manage_tags.html", tags=tags)


@admin_bp.route("/edit_tag/<int:tag_id>", methods=["GET", "POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    form = TagForm()
    if form.validate_on_submit():
        tag.name = form.name.data
        db.session.commit()
        flash("编辑成功", "success")
        return redirect(url_for("admin.manage_tags"))
    form.name.data = tag.name
    return render_template("admin/tag.html", form=form, type="编辑")


@admin_bp.route("/add_tag", methods=["GET", "POST"])
def add_tag():
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash("添加成功", "success")
        return redirect(url_for("admin.manage_tags"))
    return render_template("admin/tag.html", form=form, type="添加")


@admin_bp.route("/tag/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash("删除成功", "success")
    return redirect_back()


@admin_bp.route("/manage_posts")
def manage_posts():
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.created.desc()).paginate(page, per_page=10)

    return render_template(
        "admin/manage_posts.html",
        page=page,
        pagination=pagination,
        posts=pagination.items,
    )


@admin_bp.route("/write_post", methods=["GET", "POST"])
def write_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        content_html = request.form["fancy-editormd-html-code"]
        category = Category.query.get(form.category.data)
        tags = []
        for tag_id in form.tags.data:
            tag = Tag.query.get_or_404(tag_id)
            tags.append(tag)

        post = Post(
            title=title,
            content=content,
            content_html=content_html,
            category=category,
            tags=tags,
        )

        db.session.add(post)
        db.session.commit()
        flash("文章已发布", "success")
        return redirect(url_for("main.post", post_id=post.id))
    return render_template("admin/post.html", form=form, type="写")


@admin_bp.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.content_html = request.form["fancy-editormd-html-code"]
        post.category_id = form.category.data
        tags = []
        for tag_id in form.tags.data:
            tag = Tag.query.get_or_404(tag_id)
            tags.append(tag)
        post.tags = tags
        db.session.commit()
        flash("编辑成功", "success")
        return redirect(url_for("main.post", post_id=post_id))
    form.title.data = post.title
    form.category.data = post.category

    tag_id_list = []
    for tag in post.tags:
        tag_id_list.append(tag.id)
    form.tags.data = tag_id_list

    form.content.data = post.content

    return render_template("admin/post.html", form=form, type="编辑")


@admin_bp.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("删除成功", "success")
    return redirect_back()


@admin_bp.route("/manage_comments")
def manage_comments():
    page = request.args.get("page", 1, type=int)

    if request.args.get("filter") == "review":
        pagination = (
            Comment.query.filter_by(reviewed=False)
            .order_by(Comment.created.desc())
            .paginate(page, per_page=10)
        )
    elif request.args.get("filter") == "admin":
        pagination = (
            Comment.query.filter_by(author="admin")
            .order_by(Comment.created.desc())
            .paginate(page, per_page=10)
        )
    else:
        pagination = Comment.query.order_by(Comment.created.desc()).paginate(
            page, per_page=10
        )

    return render_template(
        "admin/manage_comments.html",
        page=page,
        pagination=pagination,
        comments=pagination.items,
        total_count=Comment.query.count(),
        review_count=Comment.query.filter_by(reviewed=False).count(),
    )


@admin_bp.route("/comment/<int:comment_id>/approve", methods=["POST"])
def approve_comment(comment_id):
    # 切换审核状态
    comment = Comment.query.get_or_404(comment_id)

    if comment.reviewed:
        comment.reviewed = False
    else:
        comment.reviewed = True

    db.session.commit()
    flash("操作成功", "success")
    return redirect_back()


@admin_bp.route("/comment/<int:comment_id>/delete", methods=["POST"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash("删除成功", "success")
    return redirect_back()


@admin_bp.route("/manage_links")
def manage_links():
    links = Link.query.all()
    return render_template("admin/manage_links.html", links=links)


@admin_bp.route("/edit_link/<int:link_id>", methods=["GET", "POST"])
def edit_link(link_id):
    link = Link.query.get_or_404(link_id)
    form = LinkForm()
    if form.validate_on_submit():
        link.name = form.name.data
        link.url = form.url.data
        db.session.commit()
        flash("编辑成功", "success")
        return redirect(url_for("admin.manage_links"))
    form.name.data = link.name
    form.url.data = link.url
    return render_template("admin/link.html", form=form, type="编辑")


@admin_bp.route("/add_link", methods=["GET", "POST"])
def add_link():
    form = LinkForm()
    if form.validate_on_submit():
        link = Link(name=form.name.data, url=form.url.data)
        db.session.add(link)
        db.session.commit()
        flash("添加成功", "success")
        return redirect(url_for("admin.manage_links"))
    return render_template("admin/link.html", form=form, type="添加")


@admin_bp.route("/link/<int:link_id>/delete", methods=["POST"])
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash("删除成功", "success")
    return redirect_back()