"""
# @File    :    models.py
# @Time    :    1/03/2022 01:36
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: model class used in flask app
"""
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from seoul_bike_flask_app import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.email} {self.password}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


user_articles = db.Table(
    "user_blog",
    db.Column("id", db.Integer, primary_key=True, autoincrement=True,
              nullable=False),
    db.Column("user_id", db.BigInteger, db.ForeignKey('user.id')),
    db.Column("blog_id", db.BigInteger, db.ForeignKey('tb_blogs.id')),
)


class Blog(db.Model):
    __tablename__ = 'tb_blogs'
    id = db.Column(db.Integer, primary_key=True, )
    title = db.Column(db.String(64), default="", unique=True)
    content = db.Column(db.Text, default="")
    create_datetime = db.Column(db.DateTime, default=datetime.now())
    user_list = db.relationship(User, secondary=user_articles,
                                backref="article_list", lazy="dynamic")


class UserBlogStars(db.Model):
    __tablename__ = 'tb_user_blog_starts'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey(User.id))
    bid = db.Column(db.Integer, db.ForeignKey(Blog.id))
    count = db.Column(db.Integer, default=0)
