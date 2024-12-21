from flask_mail import Message
from app import mail
from flask import current_app
import random
import string

def generate_verification_code():
    """生成6位验证码"""
    return ''.join(random.choices(string.digits, k=6))

def send_verification_email(email, code):
    """发送验证码邮件"""
    try:
        msg = Message(
            '【Eat What】邮箱验证码',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = f'''您好！
        
您的验证码是：{code}

验证码有效期为5分钟，请尽快完成验证。

如果这不是您的操作，请忽略此邮件。

此致
Eat What 团队'''
        
        mail.send(msg)
        print(f"验证码 {code} 已发送至 {email}")  # 添加调试信息
    except Exception as e:
        print(f"发送邮件失败: {str(e)}")  # 添加错误信息
        raise e 