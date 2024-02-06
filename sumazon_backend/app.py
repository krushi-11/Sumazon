import os
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from models import db, User
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

with app.app_context():
    db.create_all()
     # Check if there are any admin users
    admin_user = User.query.filter_by(is_admin=True).first()
    if admin_user is None:
        # Create a default admin user if none exists
        bcrypt = Bcrypt(app)
        hashed_password = bcrypt.generate_password_hash('admin@123'.encode('utf-8'))
        default_admin = User(username='admin', password=hashed_password, email='admin@sumazon.com', is_admin=True)
        db.session.add(default_admin)
        db.session.commit()

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user.id))

if __name__ == '__main__':
    from routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    app.run(debug=True, port=8000)
