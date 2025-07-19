from flask import Blueprint

subscription_bp = Blueprint('subscription', __name__)

@subscription_bp.route('/subscription')
def get_subscription():
    return "This is the subscription page."
