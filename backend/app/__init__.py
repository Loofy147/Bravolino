import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../../frontend', static_url_path='/')
    app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), '..', 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    db.init_app(app)

    with app.app_context():
        from app.routes import user, education, subscription
        app.register_blueprint(user.user_bp, url_prefix='/api')
        app.register_blueprint(education.education_bp, url_prefix='/api')
        app.register_blueprint(subscription.subscription_bp, url_prefix='/api')

        db.create_all()

    return app
