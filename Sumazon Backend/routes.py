from flask import Blueprint, request, jsonify
from auth import admin_required, token_required
from models import db, Product, CartItem, User
from utils import row_mapping_to_json

bp = Blueprint('routes', __name__)

@bp.route('/products/<int:product_id>', methods=['GET'])
@token_required
def get_product_by_id(current_user, product_id):
    if request.method == 'GET':
        product = Product.query.filter_by(id=product_id).first()
        if product:
            return jsonify({'data': product})
        else:
            return jsonify({'error': 'Product not found! Please provide valid product id'}), 204

@bp.route('/products/<int:product_id>', methods=['GET', 'DELETE', 'PUT'])
@token_required
@admin_required
def update_product_by_id(current_user, product_id):
    if request.method =='DELETE':
        product = Product.query.filter_by(id=product_id).first()
        if (product):
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully!'})
        else:
            return jsonify({'error': 'Product not found! Please provide valid product id'}), 204
    if request.method =='PUT':
        data = request.get_json()
        product = Product.query.filter_by(id=product_id).first()
        if (product):
            product.name=data['name']
            product.price=data['price']
            product.description=data['description']
            product.available_quantity=data['available_quantity']
            product.image_url=data.get('image_url')
            db.session.commit()
            return jsonify({'message': 'Product updated successfully!'})
        else:
            return jsonify({'error': 'Product not found! Please provide valid product id'}), 204
    

@bp.route('/products', methods=['GET'])
@token_required
def get_products(current_user):
        products = Product.query.all()
        return jsonify({'data': products})
    
@bp.route('/products', methods=['POST'])
@token_required
@admin_required
def add_product(current_user):
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

@bp.route('/cart/add', methods=['POST'])
@token_required
def add_to_cart(current_user):
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Check product availability
    product = Product.query.get(product_id)
    if product.available_quantity < quantity:
        return jsonify({'error': 'Not enough available quantity'}), 400
    
    # Check if item is already added in cart
    existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if (existing_item):
        existing_item.quantity = existing_item.quantity + quantity
    else:
        # Add item to cart
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    product.available_quantity = product.available_quantity - quantity
    db.session.commit()
    cart_items = CartItem.query.filter_by(user_id=current_user.id, order_id=None).all()
    return jsonify({'message': 'Item added to cart successfully', 'data': cart_items})

@bp.route('/cart/update', methods=['POST'])
@token_required
def update_cart(current_user):
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    # get existing cart item entry
    existing_product = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    previous_quantity = existing_product.quantity
    if existing_product and existing_product.quantity == quantity:
        CartItem.delete().where(user_id=current_user.id, product_id=product_id, order_id=None)
    else:
        existing_product.quantity = quantity
    
    # update the available product quantity
    product = Product.query.filter_by(id=product_id).first()
    if product:
        product.available_quantity = product.available_quantity + (previous_quantity - quantity)
    db.session.commit()
    return jsonify({'message': 'Cart updated successfully'})

@bp.route('/cart', methods=['GET'])
@token_required
def get_cart_items(current_user):
    cart_items = db.session.query(Product.id, Product.name, Product.description, Product.price, Product.image_url, CartItem.quantity).join(CartItem, Product.id == CartItem.id).filter(CartItem.user_id==current_user.id, CartItem.order_id==None).all()
    return jsonify({'message': 'Cart Items retrieved successfully!', 'data': row_mapping_to_json(cart_items)})

@bp.route('/profile/<int:user_id>', methods=['GET', 'PUT'])
@bp.route('/profile/', methods=['GET'])
@token_required
def profile(current_user, user_id=None):
    user = user_id or current_user.id
    if request.method == 'GET':
        # Return user profile information
        user_profile = User.query.filter_by(id=user).first()
        profile_data = {
            'id': current_user.id,
            'username': current_user.username,
            'email': user_profile.email,
            'address': user_profile.address,
            'phone_number': user_profile.phone_number,
            'profile_image': user_profile.profile_image,
            'is_admin': user_profile.is_admin
        }
        return jsonify({'data': profile_data})
    elif request.method == 'PUT':
        # Update user profile information
        data = request.get_json()
        user_profile = User.query.filter_by(id=user).first()
        user_profile.email = data.get('email', user_profile.email)
        user_profile.address = data.get('address', user_profile.address)
        user_profile.phone_number = data.get('phone_number', user_profile.phone_number)
        user_profile.profile_image = data.get('profile_image', user_profile.profile_image)
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'})