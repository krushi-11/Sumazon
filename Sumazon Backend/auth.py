from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, current_app, request, jsonify
from flask_bcrypt import Bcrypt
from app import app, load_user
from models import User
from models import db
import jwt

bp = Blueprint('auth', __name__)

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
                "error": "Authentication Token is missing!",
                "data": None
            }, 401
        try:
            data=jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
            if (datetime.now() > datetime.fromtimestamp(data['exp'])):
                return {
                    "error": "Token expired!",
                    "data": None
                }
            current_user=User.query.filter_by(id=data['user_id']).first()
            if current_user is None:
                return {
                "error": "Invalid Authentication token!",
                "data": None
            }, 401
        except Exception as e:
            return {
                "error": "Something went wrong",
                "data": None
            }, 403
        load_user(current_user)
        return f(current_user, *args, **kwargs)

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.is_admin:
            return f(current_user, *args, **kwargs)
        else:
            return jsonify({"error": "Admin privileges required!"}), 403

    return decorated


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    bcrypt = Bcrypt(app)
    hashed_password = bcrypt.generate_password_hash(password.encode('utf-8'))
    
    new_user = User(username=username, password=hashed_password, email=email)
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
                    {"user_id": user.id, "exp": datetime.now() + timedelta(days=1)},
                    app.config["JWT_SECRET_KEY"],
                    algorithm="HS256"
                )
        return jsonify({'message': 'Logged in successfully', 'token': token})
    else:
        return jsonify({'error': 'Invalid username or password'})

@bp.route('/logout', methods=['POST'])
def logout():
    # No user session is maintained
    return jsonify({'message': 'User logged out successfully!'})
