import random
from faker import Faker
from sqlalchemy.exc import IntegrityError
from .models import Option, User, Category, Tag, Post, Comment, Link
from .extensions import db


fake = Faker()


def fake_option():
    blog_title = Option(
        name='blog_title',
        value='空心的博客'
    )
    db.session.add(blog_title)

    blog_sub_title = Option(
        name='blog_sub_title',
        value='子标题'
    )
    db.session.add(blog_sub_title)

    blog_about = Option(
        name='blog_about',
        value='空心的个人博客'
    )
    db.session.add(blog_about)

    db.session.commit()


def fake_user():
    user = User(
        name='admin'
    )
    user.set_password('123456')

    db.session.add(user)
    db.session.commit()


def fake_categorys():
    category = Category(name='未分类')
    db.session.add(category)
    category = Category(name='Python')
    db.session.add(category)
    category = Category(name='JavaScript')
    db.session.add(category)
    category = Category(name='Electron')
    db.session.add(category)
    category = Category(name='小程序')
    db.session.add(category)
    category = Category(name='Vue')
    db.session.add(category)
    category = Category(name='SQL')
    db.session.add(category)
    category = Category(name='Linux')
    db.session.add(category)
    category = Category(name='Windows')
    db.session.add(category)
    category = Category(name='Autohotkey')
    db.session.add(category)
    db.session.commit()


def fake_tags():
    for i in range(10):
        tag = Tag(name=fake.word())
        db.session.add(tag)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  # 出错就回滚


def fake_posts():
    for i in range(7):
        post = Post(
            title=fake.sentence(),
            content=fake.text(300),
            category=Category.query.get(
                random.randint(1, Category.query.count())),
            created=fake.date_time_this_year()
        )

        tag = Tag.query.get(
            random.randint(1, Tag.query.count()))
        post.tags.append(tag)

        tag = Tag.query.get(
            random.randint(1, Tag.query.count()))
        post.tags.append(tag)

        db.session.add(post)
    db.session.commit()


def fake_comments():
    for i in range(3):
        comment = Comment(
            author=fake.name(),
            mail=fake.email(),
            url=fake.url(),
            content=fake.sentence(),
            created=fake.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    # 回复
    for i in range(2):
        comment = Comment(
            author=fake.name(),
            mail=fake.email(),
            url=fake.url(),
            content=fake.sentence(),
            created=fake.date_time_this_year(),
            replied=Comment.query.get(
                random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    twitter = Link(name='Twitter', url='#')
    facebook = Link(name='Facebook', url='#')
    linkedin = Link(name='LinkedIn', url='#')
    google = Link(name='Google+', url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()
