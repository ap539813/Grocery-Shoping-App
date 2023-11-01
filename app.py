from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import func
from datetime import datetime
import json
from flask_login import LoginManager, UserMixin, login_user, logout_user #current_user, login_required
from flask import render_template, redirect, url_for, flash
from flask_cors import CORS


app = Flask(__name__)

CORS(app, 
     origins=["http://localhost:8080"], 
     methods=["GET", "POST", "PUT"], 
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"], 
     supports_credentials=True)


with open('config.json') as config_file:
    config_data = json.load(config_file)

app.config['SECRET_KEY'] = config_data['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config_data['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

admin_creds = {'username':'admin', 'password': 'password'}



# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)

# User loader function
@login_manager.user_loader
def load_user(user_id):
    try:
        print('#'*10 + '\nUser found\n' + '#'*10)
        return User.query.get(int(user_id))
    except:
        print('#'*10 + '\nUser not found\n' + '#'*10)
    # return None

@app.route('/logout', methods=['GET'])
def logout():
    username = request.args.get('username', None)
    current_user = User.query.filter_by(username=username).first()
    if (current_user.is_authenticated):
        current_user.is_authenticated = False
        db.session.commit()
    return jsonify({"message": "Logout successful!", "status": "success"}), 200



class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_authenticated = db.Column(db.Boolean, default=False, nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True, cascade="all, delete")

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'products': [product.as_dict() for product in self.products]
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20))
    rate = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    manufacturing_date = db.Column(db.DateTime, nullable=False)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'unit': self.unit,
            'rate': self.rate,
            'quantity': self.quantity,
            'category_id': self.category_id,
            'manufacturing_date': self.manufacturing_date,
            'cart_items': [cart_item.as_dict() for cart_item in self.cart_items],

        }

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20))
    quantity = db.Column(db.Integer, default=1)
    rate = db.Column(db.Float, nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'category': self.category,
            'product_name': self.product_name,
            'unit': self.unit,
            'quantity': self.quantity,
            'rate': self.rate
        }

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
    category_id = db.Column(db.Integer, nullable=True)

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
    existing_manager_request = ApprovalRequest.query.filter_by(username = username, category = "manager").first()

    if existing_user or existing_manager or existing_manager_request:
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
    
@app.route('/create_category_request', methods=['POST'])
def create_category_request():
    data = request.json
    username = data['username']
    category = data['category']

    existing_manager = Manager.query.filter_by(username=username).first()
    if existing_manager:
        approval_request = ApprovalRequest(username=username, category = category, action="create_category")
        db.session.add(approval_request)
        db.session.commit()
        return jsonify({"status": "success", "message": "Category sent for approval to the admin!"}), 200
    else:
        return jsonify({"status": "fail", "message": "Manaer not valid!"}), 200


@app.route('/edit_category_request', methods=['POST'])
def edit_category_request():
    data = request.json
    username = data['username']
    category = data['category']
    category_id = data['category_id']

    existing_manager = Manager.query.filter_by(username=username).first()
    if existing_manager:
        approval_request = ApprovalRequest(username=username, category = category, action="edit_category", category_id = category_id)
        db.session.add(approval_request)
        db.session.commit()
        return jsonify({"status": "success", "message": "Category sent for approval to the admin!"}), 200
    else:
        return jsonify({"status": "fail", "message": "Manaer not valid!"}), 200


@app.route('/delete_category_request', methods=['POST'])
def delete_category_request():
    data = request.json
    username = data['username']
    category_id = data['category_id']

    existing_manager = Manager.query.filter_by(username=username).first()
    if existing_manager:
        approval_request = ApprovalRequest(username=username, action="delete_category", category_id = category_id)
        db.session.add(approval_request)
        db.session.commit()
        return jsonify({"status": "success", "message": "Category sent for approval to the admin!"}), 200
    else:
        return jsonify({"status": "fail", "message": "Manaer not valid!"}), 200

@app.route('/pending-requests', methods=['GET'])
def get_pending_requests():
    username = request.args.get('username', None)
    current_user = User.query.filter_by(username=username).first()

    if current_user and username == admin_creds["username"]:
        pending_requests = ApprovalRequest.query.all()
        if (current_user.is_authenticated):
            categories = Category.query.all()
            categories_list = [category.as_dict() for category in categories if category]
            for category in categories:            
                if category:
                    products_for_category = category.products
                    print(products_for_category)
            return jsonify({"categories": categories_list, 
                            "admin": username, 
                            "requests": [{"id": r.id, 
                                          "username": r.username, 
                                          "category": r.category} for r in pending_requests]})
        else:
            logout_user()
            print(current_user)
            return jsonify({"categories": None, "manager": None}), 401
    else:
        return jsonify({"categories": None, "manager": None}), 404


@app.route('/approve-request/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    request_to_approve = ApprovalRequest.query.get(request_id)
    
    if not request_to_approve:
        return jsonify({"message": "Request not found", "status": "fail"}), 404

    if request_to_approve.category == "manager":
        new_manager = Manager(username=request_to_approve.username, password=request_to_approve.password)
        new_manager_user = User(username=request_to_approve.username, password=request_to_approve.password)
        db.session.add(new_manager)
        db.session.add(new_manager_user)
        
        db.session.delete(request_to_approve)
        
        db.session.commit()

        return jsonify({"message": "Manager approved and added", "status": "success"}), 200
    if request_to_approve.action == "create_category":
        category_name = request_to_approve.category
        if not category_name:
            return jsonify({'status': 'fail', 'message': 'Category name is required'}), 400
    
        new_category = Category(name=category_name)
        
        try:
            db.session.add(new_category)
            db.session.delete(request_to_approve)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Category saved successfully'})
        except Exception as e:
            print(e)
            return jsonify({'status': 'fail', 'message': 'An error occurred: ' + str(e)}), 500
    if request_to_approve.action == "edit_category":
        category_id = request_to_approve.category_id
        category_name = request_to_approve.category
        if not category_name:
            return jsonify({'status': 'fail', 'message': 'Category name is required'}), 400
    
        try:
            # Fetching the category from the database using the category_id
            category = Category.query.get(category_id)
            
            # Checking if the category exists
            if not category:
                return jsonify({'status': 'error', 'message': 'Category not found'}), 404
            
            # Updating the category name
            category.name = category_name
            
            # Committing the changes to the database
            db.session.commit()
            
            return jsonify({'status': 'success', 'message': 'Category updated successfully!'})
        except Exception as e:
            # Handling any exceptions that occur
            return jsonify({'status': 'error', 'message': 'An error occurred: ' + str(e)}), 500
    if request_to_approve.action == "delete_category":
        category_id = request_to_approve.category_id
        try:
            # Fetching the category from the database using the category_id
            category = Category.query.get(category_id)
            
            # Checking if the category exists
            if not category:
                return jsonify({'status': 'error', "message": "Category not found!"}), 404
            
            # Deleting the category from the database
            db.session.delete(category)
            
            # Committing the changes to the database
            db.session.commit()
            
            return jsonify({'status': 'success', "message": "Category deleted successfully!"})
        except Exception as e:
            # Handling any exceptions that occur
            print(e)
            return jsonify({'status': 'error', "message": "An error occurred while deleting the category: " + str(e)}), 500
    return jsonify({"message": "Request type not handled", "status": "fail"}), 400


@app.route('/login-manager', methods=['GET', 'POST'])
def manager_login():
    data = request.json
    username = data['username']
    password = data['password']

    print(type(username), type(password))

    current_user = User.query.filter_by(username=username).first()
    manager = Manager.query.filter_by(username=username).first()

    if manager:
        if (current_user and current_user.is_authenticated):
            return jsonify({"message": "Already logged in!!", "status": "success"}), 200
            # return jsonify({"message": "Already logged in!!", "status": "fail"}), 401
            
        if current_user and current_user.password == password:
            # login_user(current_user, remember=True)
            current_user.is_authenticated = True
            db.session.commit()
            return jsonify({"message": "Login successful!", "status": "success"}), 200
        else:
            return jsonify({"message": "Invalid credentials", "status": "fail"}), 401
    else:
        return jsonify({"message": "Invalid manager", "status": "fail"}), 404


@app.route('/login_admin', methods=['POST'])
def login_admin():
    data = request.json
    username = data['username']
    password = data['password']

    current_user = User.query.filter_by(username=username).first()
    if current_user:
        if username == admin_creds["username"] and password == admin_creds["password"]:
            current_user.is_authenticated = True
            db.session.commit()
            return jsonify({"message": "Login successful!", "status": "success"}), 200
        else:
            return jsonify({"message": "Login failed. Invalid credentials.", "status": "fail"}), 401
    else:
        current_user = User(username=username, password=password, is_authenticated=True)
        if username == admin_creds["username"] and password == admin_creds["password"]:
            db.session.add(current_user)
            db.session.commit()
            return jsonify({"message": "Login successful!", "status": "success"}), 200
        else:
            return jsonify({"message": "Login failed. Invalid credentials.", "status": "fail"}), 401


@app.route('/categories', methods=['GET'])
def category():
    username = request.args.get('username', None)
    current_user = User.query.filter_by(username=username).first()
    manager = Manager.query.filter_by(username=username).first()

    if manager:
        if (current_user.is_authenticated):
            categories = Category.query.all()
            categories_list = [category.as_dict() for category in categories if category]
            for category in categories:            
                if category:
                    products_for_category = category.products
            return jsonify({"categories": categories_list, "manager": username}), 200
        else:
            print(current_user.is_authenticated)
            return jsonify({"message": "Login failed. Invalid user.", "status": "fail"}), 401
    else:
        return jsonify({"message": "Invalid manager", "status": "fail"}), 404
    
@app.route('/save_category', methods=['POST'])
def save_category():
    data = request.json
    print(data)
    category_name = data.get('category_name')
    
    if not category_name:
        return jsonify({'status': 'error', 'message': 'Category name is required'}), 400
    
    new_category = Category(name=category_name)
    
    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Category saved successfully'})
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': 'An error occurred: ' + str(e)}), 500
    
@app.route('/delete_category', methods=['POST'])
def delete_category():
    data = request.json
    try:
        # Fetching the category from the database using the category_id
        print(data)
        category = Category.query.get(data['category_id'])
        
        # Checking if the category exists
        if not category:
            return jsonify({'status': 'error', "message": "Category not found!"}), 404
        
        # Deleting the category from the database
        db.session.delete(category)
        
        # Committing the changes to the database
        db.session.commit()
        
        return jsonify({'status': 'success', "message": "Category deleted successfully!"})
    except Exception as e:
        # Handling any exceptions that occur
        print(e)
        return jsonify({'status': 'error', "message": "An error occurred while deleting the category: " + str(e)}), 500
    

@app.route('/update_category', methods=['POST'])
def update_category():
    data = request.json
    try:
        # Fetching the category from the database using the category_id
        category = Category.query.get(data['id'])
        
        # Checking if the category exists
        if not category:
            return jsonify({'status': 'error', 'message': 'Category not found'}), 404
        
        # Updating the category name
        category.name = data['name']
        
        # Committing the changes to the database
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Category updated successfully!'})
    except Exception as e:
        # Handling any exceptions that occur
        return jsonify({'status': 'error', 'message': 'An error occurred: ' + str(e)}), 500
    
@app.route('/save_product', methods=['POST'])
def save_product():
    data = request.json
    category_id = data['category_id']
    product_name = data['product_name']
    unit = data['unit']
    rate = float(data['rate'])
    quantity = int(data['quantity'])
    mfd = datetime.strptime(data['mfd'], '%Y-%m-%d')

    print(data)
    category = Category.query.get(category_id)
    print(category)
    
    if not product_name:
        return jsonify({'status': 'error', 'message': 'Product name is required'}), 400
    
    new_product = Product(
        category = category,
        name=product_name,
        unit=unit,
        rate=rate,
        quantity=quantity,
        manufacturing_date=mfd
    )
    
    try:
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Product saved successfully'})
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': 'An error occurred: ' + str(e)}), 500

@app.route('/edit_product', methods=['POST'])
def edit_product():
    data = request.get_json()
    product_id = data['product_id']
    product_name = data['product_name']
    unit = data['unit']
    rate = float(data['rate'])
    quantity = int(data['quantity'])
    mfd = datetime.strptime(data['mfd'], '%Y-%m-%d')

    # Find the product by its ID
    product = Product.query.get(product_id)

    if not product:
        return jsonify({'status': 'error', "message": "Product not found!"}), 404

    # Update the product's name
    product.name = product_name
    product.unit = unit
    product.rate = rate
    product.quantity = quantity
    product.manufacturing_date = mfd
    
    # Commit the changes to the database
    try:
        db.session.commit()
        return jsonify({'status': 'success', "message": "Product successfully edited!"}), 200
    except Exception as e:
        # Handle the exception and rollback in case of any errors
        db.session.rollback()
        return jsonify({'status': 'error', "message": "An error occurred: " + str(e)}), 500

@app.route('/delete_product', methods=['POST'])
def delete_product():
    data = request.get_json()
    print(data)
    product_id = data['product_id']

    # Find the product by its ID
    product = Product.query.get(int(product_id))

    if not product:
        return jsonify({'status': 'error', "message": "Product not found!"}), 404
    
    # Commit the changes to the database
    try:
        # Deleting the product from the database
        db.session.delete(product)
        db.session.commit()
        return jsonify({'status': 'success', "message": "Product successfully deleted!"}), 200
    except Exception as e:
        # Handle the exception and rollback in case of any errors
        db.session.rollback()
        return jsonify({'status': 'error', "message": "An error occurred: " + str(e)}), 500
    
@app.route('/add_category_', methods = ['POST'])
def save_category_request():
    pass
if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)


