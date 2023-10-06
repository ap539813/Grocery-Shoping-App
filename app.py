from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask import render_template, redirect, url_for, flash
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"], methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["Content-Type", "Authorization"], supports_credentials=True)

with open('config.json') as config_file:
    config_data = json.load(config_file)

app.config['SECRET_KEY'] = config_data['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config_data['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# @app.after_request
# def after_request(response):
#     header = response.headers
#     header['Access-Control-Allow-Origin'] = 'http://localhost:8080'
#     header['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
#     header['Access-Control-Allow-Methods'] = 'GET,POST'
#     return response



@login_manager.user_loader
def load_user(user_id):
    if Manager.query.get(int(user_id)):
        return Manager.query.get(int(user_id))
    elif User.query.get(int(user_id)):
        return User.query.get(int(user_id))
    return None

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        manager = Manager.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for("some_protected_route"))
        elif manager and manager.password == password:
            login_user(manager)
            return redirect(url_for("some_protected_route"))
        else:
            flash("Login unsuccessful. Check username and password.", "danger")
    return render_template("login.html")



class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True, cascade="all, delete")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20))
    rate = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20))
    quantity = db.Column(db.Integer, default=1)
    rate = db.Column(db.Float, nullable=False)

class Ledger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20))
    quantity = db.Column(db.Integer, default=1)
    rate = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)

class ApprovalRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    action = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"ApprovalRequest('{self.username}', '{self.category}', '{self.action}')"


with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    is_manager = data['isManager']

    existing_user = User.query.filter_by(username=username).first()
    existing_manager = Manager.query.filter_by(username=username).first()

    if existing_user or existing_manager:
        return jsonify({"message": "Username already taken!"}), 400

    if is_manager:
        approval_request = ApprovalRequest(username=username, password=password, category="manager", action="registration")
        db.session.add(approval_request)
        db.session.commit()
        return jsonify({"message": "Registration sent for approval to the admin!"}), 200
    else:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Registration successful!"}), 200




if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)


