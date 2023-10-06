from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required


app = Flask(__name__)

with open('config.json') as config_file:
    config_data = json.load(config_file)

app.config['SECRET_KEY'] = config_data['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config_data['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']  # In a real scenario, make sure to hash & salt this
    is_manager = data['isManager']

    if is_manager:
        manager = Manager(username=username, password=password)
        db.session.add(manager)
    else:
        user = User(username=username, password=password)
        db.session.add(user)

    db.session.commit()

    return jsonify({"message": "Registration successful!"}), 200


if __name__ == "__main__":
    app.run(debug=True)
