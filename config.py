import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    
    # MySQL配置
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '3306'
    MYSQL_DATABASE = 'eatwhat'
    
    # 数据库URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # 邮箱配置（使用QQ邮箱）
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True  # QQ邮箱使用SSL
    MAIL_USE_TLS = False
    MAIL_USERNAME = '2212349650@qq.com'  # 替换成你的QQ邮箱
    MAIL_PASSWORD = 'uyzqzgkllaivdjad'  # 替换成你刚才获取的授权码