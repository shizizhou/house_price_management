from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, User, Property


app = Flask(__name__)
app.secret_key = 'aabbccddeeffgghh'

engine = create_engine('sqlite:///house_price_management.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    session = Session()
    return session.query(User).get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session = Session()
        username = request.form['username']
        password = request.form['password']

        if session.query(User).filter_by(username=username).first():
            return '用户名已存在'
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session = Session()
        username = request.form['username']
        password = request.form['password']

        user = session.query(User).filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect('/')
        return render_template('login_failed.html')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    session = Session()
    properties = session.query(Property).filter_by(user_id=current_user.id).all()
    return render_template('index.html', username=current_user.username, properties=properties)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        session = Session()
        title = request.form['title']
        location = request.form['location']
        price = int(request.form['price'])
        size = int(request.form['size'])

        property = Property(
            title=title,
            location=location,
            price=price,
            size=size,
            user_id=current_user.id
        )

        session.add(property)
        session.commit()
        return redirect('/')

    return render_template('create_property.html')

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    session = Session()
    id=request.form.get('property_id')
    user_id=current_user.id
    property = session.query(Property).filter_by(id=id, user_id=user_id).first()
    if property:
        session.delete(property)
        session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

