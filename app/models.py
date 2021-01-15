from .extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    value = db.Column(db.Text)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    slug = db.Column(db.String(32), unique=True)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    password = db.Column(db.String(64))
    mail = db.Column(db.String(150))

    posts = db.relationship(
        "Post", back_populates="user", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    posts = db.relationship(
        "Post", back_populates="category", cascade="all, delete-orphan"
    )


relationshipn_table = db.Table(
    "relationship",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    posts = db.relationship(
        "Post", secondary=relationshipn_table, back_populates="tags"
    )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    read_count = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
 
    user = db.relationship("User", back_populates="posts")
    category = db.relationship("Category", back_populates="posts")
    comments = db.relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
    tags = db.relationship("Tag", secondary=relationshipn_table, back_populates="posts")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32))
    mail = db.Column(db.String(150))
    url = db.Column(db.String(255))
    content = db.Column(db.Text)
    ip = db.Column(db.String(32))
    created = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    reviewed = db.Column(db.Boolean, default=False)

    replied_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    post = db.relationship("Post", back_populates="comments")
    replies = db.relationship(
        "Comment", back_populates="replied", cascade="all, delete-orphan"
    )
    replied = db.relationship("Comment", back_populates="replies", remote_side=[id])


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    url = db.Column(db.String(255))
