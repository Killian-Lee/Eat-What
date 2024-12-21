import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    
    # MySQL配置（使用环境变量）
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'nwpu-eatwhat.mysql.database.azure.com')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', '3306'))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'Killian')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'lyk20040709.')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'eatwhat')
    
    # 数据库URI（添加 SSL 配置）
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?ssl_ca=DigiCertGlobalRootCA.crt.pem'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # 邮箱配置（使用环境变量）
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '2212349650@qq.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'uyzqzgkllaivdjad')