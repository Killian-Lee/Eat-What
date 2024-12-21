from flask import Blueprint, render_template, flash, redirect, url_for, request, session, jsonify
from app.forms import (LoginForm, EmailVerificationForm, RegistrationForm, 
                      ResetPasswordRequestForm, ResetPasswordForm, RandomSearchForm, CommentForm)
from app.models import User, Window, Canteen, Comment, Rating
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app.utils import generate_verification_code, send_verification_email
from datetime import datetime, timedelta
import random
from sqlalchemy.sql import func

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
            flash('该邮箱未注册', 'danger')
            
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

@auth_bp.route('/random', methods=['GET', 'POST'])
@login_required
def random_window():
    form = RandomSearchForm()
    
    if form.validate_on_submit():
        # 构建查询
        query = Window.query.join(Canteen)
        
        # 只有当用户选择了食堂时才筛选
        if form.canteen.data:
            query = query.filter(Canteen.name == form.canteen.data)
        # 只有当用户选择了楼层时才筛选
        if form.floor.data:
            query = query.filter(Canteen.floor == int(form.floor.data))
        # 只有当用户输入了最低价格时才筛选
        if form.min_price.data:
            query = query.filter(Window.min_price >= float(form.min_price.data))
        # 只有当用户输入了最高价格时才筛选
        if form.max_price.data:
            query = query.filter(Window.max_price <= float(form.max_price.data))
        # 只有当用户选择了最低评分时才筛选
        if form.min_rating.data:
            query = query.filter(Window.avg_rating >= float(form.min_rating.data))
            
        # 获取所有符合条件的窗口
        windows = query.all()
        
        if windows:
            # 随机选择一个窗口
            selected_window = random.choice(windows)
            return render_template('random_result.html', window=selected_window)
        else:
            flash('没有找到符合条件的窗口，请调整筛选条件', 'warning')
            
    return render_template('random.html', form=form)

# 添加AJAX路由用于动态更新楼层选项
@auth_bp.route('/get-floors/<canteen>')
def get_floors(canteen):
    floors = db.session.query(Canteen.floor).filter_by(name=canteen).all()
    return jsonify([(str(f[0]), f'{f[0]}楼') for f in floors])

@auth_bp.route('/canteens')
@login_required
def list_canteens():
    """显示所有食堂"""
    canteens = db.session.query(Canteen.name).distinct().all()
    canteen_data = {}
    
    for c in canteens:
        canteen_name = c[0]
        floors = Canteen.query.filter_by(name=canteen_name).all()
        canteen_data[canteen_name] = floors
        
    return render_template('canteens.html', canteen_data=canteen_data)

@auth_bp.route('/canteen/<name>/<int:floor>')
@login_required
def view_canteen(name, floor):
    """显示特定食堂特定楼层的窗口"""
    canteen = Canteen.query.filter_by(name=name, floor=floor).first_or_404()
    windows = Window.query.filter_by(canteen_id=canteen.id).order_by(Window.number).all()
    return render_template('canteen_detail.html', canteen=canteen, windows=windows)

@auth_bp.route('/window/<int:id>')
@login_required
def view_window(id):
    """显示窗口详情"""
    window = Window.query.get_or_404(id)
    comments = Comment.query.filter_by(window_id=id).order_by(Comment.created_at.desc()).all()
    return render_template('window_detail.html', window=window, comments=comments)

@auth_bp.route('/window/<int:id>/comment', methods=['GET', 'POST'])
@login_required
def add_comment(id):
    window = Window.query.get_or_404(id)
    form = CommentForm()
    
    if form.validate_on_submit():
        # 添加评论
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            window_id=id
        )
        db.session.add(comment)
        
        # 添加评分
        rating = Rating(
            stars=int(form.rating.data),
            user_id=current_user.id,
            window_id=id
        )
        db.session.add(rating)
        
        # 更新窗口平均评分
        window.avg_rating = (
            db.session.query(func.avg(Rating.stars))
            .filter(Rating.window_id == id)
            .scalar() or 0.0
        )
        
        db.session.commit()
        flash('评价提交成功！', 'success')
        return redirect(url_for('auth.view_window', id=id))
        
    return render_template('add_comment.html', form=form, window=window)