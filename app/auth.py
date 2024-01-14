# auth.py
from werkzeug.security import check_password_hash
from models import User  # Assuming you have a User model

def verify_login_credentials(username, password):
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        return user

    return None
