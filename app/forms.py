from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[
        DataRequired(),
        Email(),
        Regexp(r'.*@mail\.nwpu\.edu\.cn$', message='请使用西北工业大学邮箱')
    ])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class EmailVerificationForm(FlaskForm):
    email = StringField('邮箱', validators=[
        DataRequired(),
        Email(),
        Regexp(r'.*@mail\.nwpu\.edu\.cn$', message='只允许使用西北工业大学邮箱')
    ])
    submit = SubmitField('发送验证码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

class RegistrationForm(FlaskForm):
    verification_code = StringField('验证码', validators=[
        DataRequired(),
        Length(min=6, max=6, message='请输入6位验证码')
    ])
    username = StringField('用户名', validators=[
        DataRequired(),
        Length(min=3, max=20, message='用户名长度必须在3-20位之间')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(),
        Length(min=6, max=16, message='密码长度必须在6-16位之间')
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(),
        EqualTo('password', message='两次输入的密码不匹配')
    ])
    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[
        DataRequired(),
        Email(),
        Regexp(r'.*@mail\.nwpu\.edu\.cn$', message='请输入注册时使用的西北工业大学邮箱')
    ])
    submit = SubmitField('发送验证码')

class ResetPasswordForm(FlaskForm):
    verification_code = StringField('验证码', validators=[
        DataRequired(),
        Length(min=6, max=6, message='请输入6位验证码')
    ])
    password = PasswordField('新密码', validators=[
        DataRequired(),
        Length(min=6, max=16, message='密码长度必须在6-16位之间')
    ])
    confirm_password = PasswordField('确认新密码', validators=[
        DataRequired(),
        EqualTo('password', message='两次输入的密码不匹配')
    ])
    submit = SubmitField('重置密码')

class RandomSearchForm(FlaskForm):
    canteen = SelectField('食堂', choices=[
        ('', '请选择食堂'),
        ('星南', '星南'),
        ('星北', '星北'),
        ('云餐', '云餐')
    ])
    floor = SelectField('楼层', choices=[
        ('', '请选择楼层'),
        ('2', '2楼'),
        ('3', '3楼')
    ])
    min_price = StringField('最低价格')
    max_price = StringField('最高价格')
    min_rating = SelectField('最低评分', choices=[
        ('', '请选择最低评分'),
        ('1', '1星'),
        ('2', '2星'),
        ('3', '3星'),
        ('4', '4星'),
        ('5', '5星')
    ])
    submit = SubmitField('随机选择')

class CommentForm(FlaskForm):
    content = TextAreaField('评论内容', validators=[
        DataRequired(message='评论内容不能为空'),
        Length(min=1, max=500, message='评论长度必须在1-500字之间')
    ])
    rating = SelectField('评分', choices=[
        ('1', '1星'),
        ('2', '2星'),
        ('3', '3星'),
        ('4', '4星'),
        ('5', '5星')
    ], validators=[DataRequired(message='请选择评分')])
    submit = SubmitField('提交评价')
  