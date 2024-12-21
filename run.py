from app import create_app, db
import pymysql
from init_data import init_canteens_and_windows
import os

app = create_app()

def init_db():
    """初始化数据库"""
    try:
        print("开始初始化数据库...")
        
        # 连接MySQL（添加SSL配置）
        conn = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            port=app.config['MYSQL_PORT'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            ssl={
                'ca': 'DigiCertGlobalRootCA.crt.pem'
            }
        )
        print("数据库连接成功")
        
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {app.config['MYSQL_DATABASE']} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"数据库 {app.config['MYSQL_DATABASE']} 创建成功")
        
        cursor.close()
        conn.close()

        with app.app_context():
            print("开始创建表...")
            db.create_all()
            print("表创建成功")
            
            from app.models import Canteen
            if not Canteen.query.first():
                print("初始化基础数据...")
                init_canteens_and_windows()
                print("基础数据初始化完成")
    except Exception as e:
        print(f"初始化过程出错: {str(e)}")
        raise e

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)
else:
    print("通过 gunicorn 启动，初始化数据库...")
    init_db()