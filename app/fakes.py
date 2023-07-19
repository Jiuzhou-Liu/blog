import random
from faker import Faker
from sqlalchemy.exc import IntegrityError
from .models import Option, Page, User, Category, Tag, Post, Comment, Link
from .extensions import db


fake = Faker()


def fake_option():
    db.session.add_all(
        [
            Option(name="blog_title", value="空心's Blog"),
            Option(name="blog_sub_title", value="子标题"),
            Option(
                name="blog_navbar",
                value="""\
                <a href="https://github.com/zero-ljz/"><svg class="octicon octicon-mark-github v-align-middle" height="32" viewBox="0 0 16 16" version="1.1" width="32" aria-hidden="true"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg></a>
                """,
            ),
            Option(
                name="blog_footer",
                value="""\
                <p><small><a target="_blank" href="http://beian.miit.gov.cn">湘ICP备00000000号</a><br/>
            <a target="_blank" href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=00000000000000"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAMAAAC6V+0/AAABjFBMVEVHcEzoxWzs04visWL++9725r7dpFXitWH89t337Lr52Ifov3f25qPcsX7gqlb06Zzu46rewXLlvHCdaFjvvl/crGrgvov387jz6ZLt3oDkvFnTk3DKhFvZr4LDfz7oxnzv2X//+dD/74ati3q0lH7Rrnbou1Doulr/1ljVPCLqv1fuzGbVHhjbSScFAWMAAXgBAW3ryFzksVHWj0nSBQnlmDpzd4Dpx2PdmEbrsEnw13TrwWDdn0U8GTzVazK5kVqYeljIIhDMAALKPSO9BA79xU3UxXXrXyNtf4/90GjqcDKRinm+TiUABn756XDepEz1x1f74mzVkjzThT3TLhyrq4LjrUr8lzlRNlHdhDX1fy6ZXzNdXG9NB0TXYTHQFg3XdTjyy27pgj69qXHekET/ulXBvIN0Y2HPuX+clYT2qjwZN5DuvlDx02nYnljNrFJWTm/JWSrZAAZgHlCxDg79KwoAG45pAjaEj5n9LRTEazOBWDqEaUriqVfbbTc2Gk2njVnOeDq1gD8ACJEMcLh/AAAAJnRSTlMA7JHrCGHK/hxBusIqreg9f/XQ+dLgnAKr4fQUXUic++xMvtHLbxvU4Y4AAAFpSURBVBjTY2CAAA5WFWVWDnEGJMDJKxxdXeMgzKuIEGOxt42ucvdiD7W1Z4GJcXBHOESZaOqahIdGcEFFeQTrY6J0dEJ04108zeoZecCC/N6+De4mIfHxmk7uaQbeYEEOEW/9Jt0iHU1NHSdNNwMzJZAbVLMyfe2jTAqDtFLivdwMMjUEgCrFTDOa0119nO0S6owD0/XTssSAKkUjE7MNfJJ0neM0veL0sq1MRYEq+RpTPfRLSuN8EpIqXQw8XIOBguK8Np4ZZbEljo6Ous7l+hme6kxAQe6UWs8KAz292GI9A30zDfYwbnEGcfk8Y9PEDAeP5PyYAjNtUwsjBaCZrOr+xnYBGhqulhp+GpHGRoacINezSmkFB2mrG6lr51oYazNyQsJN1NBQXcvQWlvLRt3KnI8fHKhcflbsRuph1moW/urq5n4SkNBkklILyLFUs9QKUDOXFICGvri0jBwbGx8zGzeTLFgIAGesR4U7iOtUAAAAAElFTkSuQmCC"/>  湘公网安备 00000000000000号</a>
          </small></p>
          """,
            ),
            Option(name="sidebar_comment", value=False),
            Option(name="comment_review", value=False),
        ]
    )
    db.session.commit()


def fake_pages():

    db.session.add_all(
        [
            Page(
                title="关于",
                slug="about",
                content="""<pre><address>空心的个人博客
地区：湖南
邮箱：<a href="mailto:zero-ljz@qq.com">zero-ljz@qq.com</a>
</address></pre>""",
                created=fake.date_time_this_year(),
            ),
        ]
    )
    db.session.commit()


def fake_user():
    user = User(name="admin", mail="2267719005@qq.com")
    user.set_password("123456")

    db.session.add(user)
    db.session.commit()
    
    user = User(name="admin2", mail="22677190052@qq.com")
    user.set_password("123456")

    db.session.add(user)
    db.session.commit()
    
    user = User(name="admin3", mail="22677190053@qq.com")
    user.set_password("123456")

    db.session.add(user)
    db.session.commit()


def fake_categories():
    db.session.add_all(
        [
            Category(name="未分类"),
            Category(name="编程"),
            Category(name="Windows"),
            Category(name="Linux"),
            Category(name="Python"),
            Category(name="JavaScript"),
            Category(name="Database"),
        ]
    )

    db.session.commit()


def fake_tags():
    db.session.add_all(
        [
            Tag(name="资源"),
            Tag(name="经验"),
            Tag(name="教程"),
            Tag(name="Autohotkey"),
            Tag(name="Flask"),
            Tag(name="Scrapy"),
            Tag(name="PyQt"),
            Tag(name="MySQL"),
            Tag(name="Redis"),
        ]
    )

    db.session.commit()


def fake_posts():
    
    for i in range(103):
        post = Post(
            title=fake.sentence(),
            content=fake.text(1200),
            content_html=fake.text(1200),
            category=Category.query.get(random.randint(1, Category.query.count())),
            created=fake.date_time_this_year(),
            user_id=1,
        )

        tag = Tag.query.get(random.randint(1, Tag.query.count()))
        post.tags.append(tag)

        tag = Tag.query.get(random.randint(1, Tag.query.count()))
        post.tags.append(tag)

        db.session.add(post)
    

    db.session.add_all(
        [
            Post(
                title="世界，您好！",
                content="欢迎使用Onelog，这是您的第一篇文章，编辑或删除它，然后开始写作吧！",
                content_html="欢迎使用Onelog，这是您的第一篇文章，编辑或删除它，然后开始写作吧！",
                user=User.query.get(1),
                category=Category.query.get(1),
                created=fake.date_time_this_year(),
            ),
        ]
    )
    db.session.commit()
    
    db.session.add_all(
        [
            Post(
                title="世界，您好！2",
                content="欢迎使用Onelog，这是您的第一篇文章，编辑或删除它，然后开始写作吧！2",
                content_html="欢迎使用Onelog，这是您的第一篇文章，编辑或删除它，然后开始写作吧！2",
                user=User.query.get(1),
                category=Category.query.get(1),
                created=fake.date_time_this_year(),
            ),
        ]
    )
    db.session.commit()
    
    db.session.add_all(
        [
            Post(
                title="世界，您好！3",
                content="欢迎使用Onelog，这是您的第一篇文章，编辑或删除它，然后开始写作吧！3",
                content_html="欢迎使用Onelog，这是您的第一篇文章，编辑或删除它，然后开始写作吧！3",
                user=User.query.get(1),
                category=Category.query.get(1),
                created=fake.date_time_this_year(),
            ),
        ]
    )
    db.session.commit()


def fake_comments():
    for i in range(15):
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
    for i in range(15):
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
            Link(name="网易云", url="https://music.163.com/#/user/home?id=484667076"),
        ]
    )
    db.session.commit()
