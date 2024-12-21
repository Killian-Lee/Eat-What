from app import create_app, db
from app.models import Window, Canteen

app = create_app()

def add_windows():
    with app.app_context():
        # 获取星南3楼
        canteen = Canteen.query.filter_by(name='星南', floor=3).first()
        if canteen:
            # 添加新窗口
            new_windows = [
                Window(
                    number=11,
                    name='品忆味手工水饺',
                    canteen_id=canteen.id,
                    min_price=10.0,
                    max_price=30.0,
                    avg_rating=3.8
                ),
                Window(
                    number=12,
                    name='解馋酱骨饭',
                    canteen_id=canteen.id,
                    min_price=10.0,
                    max_price=30.0,
                    avg_rating=4.7
                )
            ]
            
            db.session.add_all(new_windows)
            db.session.commit()
            print("新窗口添加成功！")
        else:
            print("找不到星南3楼！")

if __name__ == '__main__':
    add_windows() 