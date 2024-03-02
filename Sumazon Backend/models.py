from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

@dataclass
class User(UserMixin, db.Model):
    id: int
    username: str
    password: str
    email: str
    address: str
    phone_number: str
    profile_image: str
    is_admin: bool
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    profile_image = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)

@dataclass
class Product(UserMixin, db.Model):
    id: int
    name: str
    price: float
    description: str
    available_quantity: int
    image_url: str
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

@dataclass
class CartItem(UserMixin, db.Model):
    id: int
    user_id: int
    product_id: int
    order_id: int
    quantity: int
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    
@dataclass
class Order(UserMixin, db.Model):
    id: int
    user_id: int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
