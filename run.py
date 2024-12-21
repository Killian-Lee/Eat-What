from app import create_app, db
import pymysql
from init_data import init_canteens_and_windows

app = create_app()

def init_db():
    """初始化数据库"""
    print("开始初始化数据库...")
    
    # 连接MySQL
    conn = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        port=app.config['MYSQL_PORT'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD']
    )
    cursor = conn.cursor()

    # 创建数据库（如果不存在）
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {app.config['MYSQL_DATABASE']} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print(f"数据库 {app.config['MYSQL_DATABASE']} 创建成功")
    
    cursor.close()
    conn.close()

    # 创建表
    with app.app_context():
        print("开始创建表...")
        # 先删除所有表（如果存在）
        db.drop_all()
        # 创建所有表
        db.create_all()
        print("表创建成功")
        # 初始化基础数据
        print("开始初始化基础数据...")
        init_canteens_and_windows()
        print("基础数据初始化完成")

if __name__ == '__main__':
    init_db()  # 初始化数据库
    
    # 验证表是否创建成功
    with app.app_context():
        # 连接到指定的数据库
        conn = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            port=app.config['MYSQL_PORT'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE']
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("\n创建的表:")
        for table in tables:
            print(f"- {table[0]}")
        cursor.close()
        conn.close()
    
    app.run(debug=True)