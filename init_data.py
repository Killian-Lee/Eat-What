from app import create_app, db
from app.models import Canteen, Window

def init_canteens_and_windows():
    app = create_app()
    with app.app_context():
        # 清空现有数据
        Window.query.delete()
        Canteen.query.delete()
        
        # 创建食堂数据
        canteens_data = [
            # 星南食堂
            {'name': '星南', 'floor': 2},
            {'name': '星南', 'floor': 3},
            # 星北食堂
            {'name': '星北', 'floor': 1},
            {'name': '星北', 'floor': 2},
            {'name': '星北', 'floor': 3},
            # 云餐食堂
            {'name': '云餐', 'floor': 1},
            {'name': '云餐', 'floor': 2},
        ]
        
        for data in canteens_data:
            canteen = Canteen(name=data['name'], floor=data['floor'])
            db.session.add(canteen)
            db.session.flush()  # 获取ID
            
            # 为每个食堂创建10个窗口
            for i in range(1, 11):
                window = Window(
                    number=i,
                    name=f"{data['name']}{data['floor']}楼{i}号窗口",
                    canteen_id=canteen.id,
                    min_price=10.0,  # 默认价格范围
                    max_price=30.0
                )
                db.session.add(window)
        
        db.session.commit()

if __name__ == '__main__':
    init_canteens_and_windows() 