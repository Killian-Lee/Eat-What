from app import create_app
from app.utils import send_verification_email, generate_verification_code

app = create_app()

with app.app_context():
    try:
        # 生成验证码
        code = generate_verification_code()
        # 发送到测试邮箱（这里替换成你想测试的邮箱地址）
        test_email = 'test@mail.nwpu.edu.cn'  # 替换成你要测试的邮箱
        
        print(f"正在发送验证码 {code} 到 {test_email}")
        send_verification_email(test_email, code)
        print("邮件发送成功！")
    except Exception as e:
        print(f"发送失败: {str(e)}") 