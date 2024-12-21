from app import create_app, db
import pymysql
from init_data import init_canteens_and_windows
import os

app = create_app()

def init_db():
    """初始化数据库"""
    print("开始初始化数据库...")
    
    # 连接MySQL（添加SSL配置）
    conn = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        port=app.config['MYSQL_PORT'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        ssl={
            'ca': 'DigiCertGlobalRootCA.crt.pem'  # SSL证书路径
        }
    )
    cursor = conn.cursor()

    # 创建数据库（如果不存在）
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {app.config['MYSQL_DATABASE']} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print(f"数据库 {app.config['MYSQL_DATABASE']} 创建成功")
    
    cursor.close()
    conn.close()

    # 创建表
    with app.app_context():
        print("检查并创建表...")
        db.create_all()
        print("表创建/更新成功")
        
        # 检查是否需要初始化食堂数据
        from app.models import Canteen
        if not Canteen.query.first():
            print("开始初始化基础数据...")
            init_canteens_and_windows()
            print("基础数据初始化完成")
        else:
            print("食堂数据已存在，跳过初始化")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)