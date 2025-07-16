from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS, cross_origin
from model import Base, User, Property

app = Flask(__name__)
app.secret_key = 'aabbccddeeffgghh'

engine = create_engine('sqlite:///house_price_management.db', connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

@login_manager.user_loader
def load_user(user_id):
    session = Session()
    return session.query(User).get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return jsonify({'message': '未登录'}), 401

@app.route('/api/register', methods=['POST'])
@cross_origin(origins="http://localhost:5173", supports_credentials=True)
def register():
    session = Session()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if session.query(User).filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 409

    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    return jsonify({'message': '注册成功'})

@app.route('/api/login', methods=['POST', 'OPTIONS'])
@cross_origin(origins="http://localhost:5173", supports_credentials=True)
def login():
    if request.method == 'OPTIONS':
        return '', 200  

    session = Session()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = session.query(User).filter_by(username=username).first()
    if user and user.password == password:
        login_user(user)
        return jsonify({'message': '登录成功'})
    return jsonify({'message': '用户名或密码错误'}), 401

@app.route('/api/logout', methods=['POST'])
@cross_origin(origins="http://localhost:5173", supports_credentials=True)
@login_required
def logout():
    logout_user()
    return jsonify({'message': '已退出登录'})

@app.route('/api/properties', methods=['GET'])
@cross_origin(origins="http://localhost:5173", supports_credentials=True)
@login_required
def get_properties():
    session = Session()
    properties = session.query(Property).filter_by(user_id=current_user.id).all()
    result = [
        {
            'id': p.id,
            'title': p.title,
            'location': p.location,
            'price': p.price,
            'size': p.size
        } for p in properties
    ]
    return jsonify({'username': current_user.username, 'properties': result})

@app.route('/api/create', methods=['POST'])
@cross_origin(origins="http://localhost:5173", supports_credentials=True)
@login_required
def create_property():
    session = Session()
    data = request.get_json()
    title = data.get('title')
    location = data.get('location')
    price = int(data.get('price'))
    size = int(data.get('size'))

    property = Property(
        title=title,
        location=location,
        price=price,
        size=size,
        user_id=current_user.id
    )

    session.add(property)
    session.commit()
    return jsonify({'message': '房产创建成功'})

@app.route('/api/delete', methods=['POST'])
@cross_origin(origins="http://localhost:5173", supports_credentials=True)
@login_required
def delete_property():
    session = Session()
    data = request.get_json()
    property_id = data.get('property_id')

    property = session.query(Property).filter_by(id=property_id, user_id=current_user.id).first()
    if property:
        session.delete(property)
        session.commit()
        return jsonify({'message': '删除成功'})
    return jsonify({'message': '未找到房产'}), 404

@app.route('/')
@cross_origin(origins="http://localhost:5173")
def index():
    return '🎉 Flask 后端已启动，前端请访问 http://localhost:5173'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)