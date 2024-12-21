from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)  # 邮箱
    username = db.Column(db.String(64), unique=True, nullable=False)  # 用户名
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='author', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Canteen(db.Model):
    __tablename__ = 'canteens'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # 星南、星北、云餐
    floor = db.Column(db.Integer, nullable=False)    # 楼层
    windows = db.relationship('Window', backref='canteen', lazy=True)

class Window(db.Model):
    __tablename__ = 'windows'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)  # 窗口号（1-10）
    name = db.Column(db.String(100))               # 窗口名称
    canteen_id = db.Column(db.Integer, db.ForeignKey('canteens.id'), nullable=False)
    min_price = db.Column(db.Float)                # 最低价格
    max_price = db.Column(db.Float)                # 最高价格
    avg_rating = db.Column(db.Float, default=0.0)  # 平均评分
    comments = db.relationship('Comment', backref='window', lazy=True)
    ratings = db.relationship('Rating', backref='window', lazy=True)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    window_id = db.Column(db.Integer, db.ForeignKey('windows.id'), nullable=False)

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable=False)  # 1-5星
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    window_id = db.Column(db.Integer, db.ForeignKey('windows.id'), nullable=False) 