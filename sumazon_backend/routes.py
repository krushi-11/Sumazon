from datetime import datetime, timedelta
from functools import wraps
from flask import current_app
from flask_bcrypt import Bcrypt
from flask import Blueprint, request, jsonify
from models import db, Product, CartItem, User
from app import app, load_user
import jwt

bp = Blueprint('routes', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        parts = []
        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split(" ")
        if len(parts)>1:
            token = parts[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
            if (datetime.now() > datetime.fromtimestamp(data['exp'])):
                return {
                    "message": "Token expired!",
                    "data": None,
                    "error": "Unauthorized"
                }
            current_user=User.query.filter_by(id=data['user_id']).first()
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 403
        load_user(current_user)
        return f(current_user, *args, **kwargs)

    return decorated

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    bcrypt = Bcrypt(app)
    hashed_password = bcrypt.generate_password_hash(password.encode('utf-8'))
    
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'})

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    bcrypt = Bcrypt(app)
    
    if user and bcrypt.check_password_hash(user.password, password):
        load_user(user)
        token = jwt.encode(
                    {"user_id": user.id, "exp": datetime.now() + timedelta(minutes=5)},
                    app.config["JWT_SECRET_KEY"],
                    algorithm="HS256"
                )
        return jsonify({'message': 'Logged in successfully', 'token': token})
    else:
        return jsonify({'message': 'Invalid username or password'})

@bp.route('/logout', methods=['GET'])
def logout():
    # No user session is maintained
    return jsonify({'message': 'User logged out successfully!'})

@bp.route('/products', methods=['GET'])
@token_required
def get_products(current_user):
        products = Product.query.all()
        return jsonify({'data': products})

@bp.route('/admin/products', methods=['POST'])
@token_required
def add_product(current_user):
    if current_user.is_admin:
        data = request.get_json()
        new_product = Product(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            available_quantity=data['available_quantity'],
            image_url=data.get('image_url')
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'})
    else:
        return jsonify({'message': 'Admin privileges required'}), 403

@bp.route('/cart/add', methods=['POST'])
@token_required
def add_to_cart(current_user):
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Check product availability
    product = Product.query.get(product_id)
    if product.available_quantity < quantity:
        return jsonify({'message': 'Not enough available quantity'}), 400
    
    # Check if item is already added in cart
    existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if (existing_item):
        existing_item.quantity = existing_item.quantity + quantity
    else:
        # Add item to cart
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    db.session.commit()
    cart_items = CartItem.query.filter_by(user_id=current_user.id, order_id=None).all()
    return jsonify({'message': 'Item added to cart successfully', 'data': cart_items})

@bp.route('/cart', methods=['GET'])
@token_required
def get_cart_items(current_user):
    cart_items = db.session.query(CartItem, Product).filter(CartItem.product_id==Product.id, CartItem.user_id==current_user.id, CartItem.order_id==None).all()
    return jsonify({'message': 'Cart Items retrieved successfully!', 'data': cart_items})

@bp.route('/profile', methods=['GET', 'PUT'])
@token_required
def profile(current_user):
    if request.method == 'GET':
        # Return user profile information
        user_profile = User.query.filter_by(id=current_user.id).first()
        profile_data = {
            'username': current_user.username,
            'email': user_profile.email,
            'address': user_profile.address,
            'phone_number': user_profile.phone_number,
            'profile_image': user_profile.profile_image,
            'is_admin': user_profile.is_admin
        }
        return jsonify(profile_data)
    elif request.method == 'PUT':
        # Update user profile information
        data = request.get_json()
        user_profile = User.query.filter_by(id=current_user.id).first()
        user_profile.email = data.get('email', user_profile.email)
        user_profile.address = data.get('address', user_profile.address)
        user_profile.phone_number = data.get('phone_number', user_profile.phone_number)
        user_profile.profile_image = data.get('profile_image', user_profile.profile_image)
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'})