from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from app.forms import (LoginForm, EmailVerificationForm, RegistrationForm, 
                      ResetPasswordRequestForm, ResetPasswordForm)
from app.models import User
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app.utils import generate_verification_code, send_verification_email
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.welcome'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('邮箱或密码错误', 'danger')
            return render_template('login.html', form=form)
            
        login_user(user, remember=form.remember_me.data)
        flash('登录成功！', 'success')
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth.welcome')
        return redirect(next_page)
        
    return render_template('login.html', form=form)

@auth_bp.route('/register-email', methods=['GET', 'POST'])
def register_email():
    if current_user.is_authenticated:
        return redirect(url_for('auth.welcome'))
    
    form = EmailVerificationForm()
    if form.validate_on_submit():
        verification_code = generate_verification_code()
        session['verification_code'] = verification_code
        session['verification_email'] = form.email.data
        session['verification_expiration'] = (datetime.utcnow() + timedelta(minutes=5)).timestamp()
        
        try:
            send_verification_email(form.email.data, verification_code)
            flash('验证码已发送到您的邮箱，请查收', 'success')
            return redirect(url_for('auth.register'))
        except Exception as e:
            flash('发送验证码失败，请稍后重试', 'danger')
            
    return render_template('register_email.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.welcome'))
        
    if 'verification_code' not in session:
        return redirect(url_for('auth.register_email'))
        
    if datetime.utcnow().timestamp() > session['verification_expiration']:
        flash('验证码已过期，请重新获取', 'danger')
        return redirect(url_for('auth.register_email'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.verification_code.data != session['verification_code']:
            flash('验证码错误', 'danger')
            return render_template('register.html', form=form)
            
        user = User(
            email=session['verification_email'],
            username=form.username.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # 清除session
        session.pop('verification_code', None)
        session.pop('verification_email', None)
        session.pop('verification_expiration', None)
        
        flash('注册成功！请登录', 'success')
        return redirect(url_for('auth.login'))
            
    return render_template('register.html', form=form)

@auth_bp.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('auth.welcome'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            verification_code = generate_verification_code()
            session['reset_code'] = verification_code
            session['reset_email'] = form.email.data
            session['reset_expiration'] = (datetime.utcnow() + timedelta(minutes=5)).timestamp()
            
            try:
                send_verification_email(form.email.data, verification_code)
                flash('验证码已发送到您的邮箱，请查收', 'success')
                return redirect(url_for('auth.reset_password'))
            except Exception as e:
                flash('发送验证码失败，请稍后重试', 'danger')
        else:
            flash('该邮箱未注���', 'danger')
            
    return render_template('reset_password_request.html', form=form)

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('auth.welcome'))
        
    if 'reset_code' not in session:
        return redirect(url_for('auth.reset_password_request'))
        
    if datetime.utcnow().timestamp() > session['reset_expiration']:
        flash('验证码已过期，请重新获取', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if form.verification_code.data != session['reset_code']:
            flash('验证码错误', 'danger')
            return render_template('reset_password.html', form=form)
            
        user = User.query.filter_by(email=session['reset_email']).first()
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            
            # 清除session
            session.pop('reset_code', None)
            session.pop('reset_email', None)
            session.pop('reset_expiration', None)
            
            flash('密码已重置，请使用新密码登录', 'success')
            return redirect(url_for('auth.login'))
            
    return render_template('reset_password.html', form=form)