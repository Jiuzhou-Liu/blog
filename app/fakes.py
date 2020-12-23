import random
from faker import Faker
from sqlalchemy.exc import IntegrityError
from .models import Option, User, Category, Tag, Post, Comment, Link
from .extensions import db


fake = Faker()


def fake_option():
    db.session.add_all(
        [
            Option(name="blog_title", value="空心的博客"),
            Option(name="blog_sub_title", value="子标题"),
            Option(
                name="blog_about",
                value="""<pre><address>
空心的个人博客
地区：湖南衡阳
邮箱：<a href="mailto:2267719005@qq.com">2267719005@qq.com</a>
</address></pre>""",
            ),
            Option(
                name="blog_footer",
                value="""<p><small><a target="_blank" href="http://beian.miit.gov.cn">湘ICP备17017294号</a><br/>
            <a target="_blank" href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=43012102000215"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAMAAAC6V+0/AAABjFBMVEVHcEzoxWzs04visWL++9725r7dpFXitWH89t337Lr52Ifov3f25qPcsX7gqlb06Zzu46rewXLlvHCdaFjvvl/crGrgvov387jz6ZLt3oDkvFnTk3DKhFvZr4LDfz7oxnzv2X//+dD/74ati3q0lH7Rrnbou1Doulr/1ljVPCLqv1fuzGbVHhjbSScFAWMAAXgBAW3ryFzksVHWj0nSBQnlmDpzd4Dpx2PdmEbrsEnw13TrwWDdn0U8GTzVazK5kVqYeljIIhDMAALKPSO9BA79xU3UxXXrXyNtf4/90GjqcDKRinm+TiUABn756XDepEz1x1f74mzVkjzThT3TLhyrq4LjrUr8lzlRNlHdhDX1fy6ZXzNdXG9NB0TXYTHQFg3XdTjyy27pgj69qXHekET/ulXBvIN0Y2HPuX+clYT2qjwZN5DuvlDx02nYnljNrFJWTm/JWSrZAAZgHlCxDg79KwoAG45pAjaEj5n9LRTEazOBWDqEaUriqVfbbTc2Gk2njVnOeDq1gD8ACJEMcLh/AAAAJnRSTlMA7JHrCGHK/hxBusIqreg9f/XQ+dLgnAKr4fQUXUic++xMvtHLbxvU4Y4AAAFpSURBVBjTY2CAAA5WFWVWDnEGJMDJKxxdXeMgzKuIEGOxt42ucvdiD7W1Z4GJcXBHOESZaOqahIdGcEFFeQTrY6J0dEJ04108zeoZecCC/N6+De4mIfHxmk7uaQbeYEEOEW/9Jt0iHU1NHSdNNwMzJZAbVLMyfe2jTAqDtFLivdwMMjUEgCrFTDOa0119nO0S6owD0/XTssSAKkUjE7MNfJJ0neM0veL0sq1MRYEq+RpTPfRLSuN8EpIqXQw8XIOBguK8Np4ZZbEljo6Ous7l+hme6kxAQe6UWs8KAz292GI9A30zDfYwbnEGcfk8Y9PEDAeP5PyYAjNtUwsjBaCZrOr+xnYBGhqulhp+GpHGRoacINezSmkFB2mrG6lr51oYazNyQsJN1NBQXcvQWlvLRt3KnI8fHKhcflbsRuph1moW/urq5n4SkNBkklILyLFUs9QKUDOXFICGvri0jBwbGx8zGzeTLFgIAGesR4U7iOtUAAAAAElFTkSuQmCC"/>  湘公网安备 43012102000215号</a>
          </small></p>""",
            ),
            Option(name="sidebar_comment", value=False),
            Option(name="comment_review", value=False),
        ]
    )
    db.session.commit()


def fake_user():
    user = User(name="admin", mail="2267719005@qq.com") 
    user.set_password("123456")

    db.session.add(user)
    db.session.commit()


def fake_categories():

    db.session.add_all(
        [
            Category(name="未分类"),
            Category(name="杂谈"),
            Category(name="Windows"),
            Category(name="Linux"),
            Category(name="Python"),
            Category(name="Golang"),
            Category(name="HTML/CSS"),
            Category(name="JavaScript"),
            Category(name="数据库"),
        ]
    )

    db.session.commit()


def fake_tags():
    db.session.add_all(
        [
            Tag(name="资源分享"),
            Tag(name="经验分享"),
            Tag(name="原创程序"),
            Tag(name="Autohotkey"),
            Tag(name="网络爬虫"),
            # Tag(name="自动化"),
            # Tag(name="Shell"),
            # Tag(name="Nginx"),
            Tag(name="Docker"),
            Tag(name="Flask"),
            Tag(name="Bootstrap"),
            Tag(name="jQuery"),
            Tag(name="Vue.js"),
            # Tag(name="Node.js"),
            # Tag(name="Electron"),
            # Tag(name="小程序"),
            Tag(name="SQLAlchemy"),
            Tag(name="MongoEngine"),
            Tag(name="MySQL"),
            # Tag(name="SQLite"),
            Tag(name="MongoDB"),
            Tag(name="Redis"),
            Tag(name="网络编程"),
            # Tag(name="多线程"),
            # Tag(name="消息队列"),
        ]
    )

    db.session.commit()


def fake_posts():
    for i in range(50):
        post = Post(
            title=fake.sentence(),
            content=fake.text(1200),
            category=Category.query.get(random.randint(1, Category.query.count())),
            created=fake.date_time_this_year(),
        )

        tag = Tag.query.get(random.randint(1, Tag.query.count()))
        post.tags.append(tag)

        tag = Tag.query.get(random.randint(1, Tag.query.count()))
        post.tags.append(tag)

        db.session.add(post)
    db.session.commit()


def fake_comments():
    for i in range(150):
        comment = Comment(
            author=fake.name(),
            mail=fake.email(),
            url=fake.url(),
            content=fake.sentence(),
            created=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count())),
        )
        db.session.add(comment)

    # 回复
    for i in range(150):
        comment = Comment(
            author=fake.name(),
            mail=fake.email(),
            url=fake.url(),
            content=fake.sentence(),
            created=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count())),
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():

    db.session.add_all(
        [
            Link(name="我的Github", url="https://github.com/pythoneer-ljz/"),
            Link(name="我的知乎", url="https://www.zhihu.com/people/liu-jiu-zhou-32-18"),
            Link(name="我的网易云", url="https://music.163.com/#/user/home?id=484667076"),
        ]
    )
    db.session.commit()
