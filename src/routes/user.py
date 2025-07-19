from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route('/users')
def get_users():
    return "This is the user page."
