from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class UserRole(Enum):
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"
    DEVELOPER = "developer"
    CONTENT_CREATOR = "content_creator"
    MARKETER = "marketer"
    INVESTOR = "investor"
    ADMIN = "admin"

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    
    # Profile information
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    
    # Role and status
    role = db.Column(db.Enum(UserRole), default=UserRole.STUDENT)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Referral system
    referral_code = db.Column(db.String(20), unique=True)
    referred_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    subscriptions = db.relationship('UserSubscription', backref='user', lazy=True)
    points = db.relationship('BravolinoPoints', backref='user', lazy=True, uselist=False)
    referrals_made = db.relationship('Referral', foreign_keys='Referral.referrer_id', backref='referrer', lazy=True)
    referrals_received = db.relationship('Referral', foreign_keys='Referral.referred_id', backref='referred', lazy=True)
    investments = db.relationship('Investment', backref='investor', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role.value if self.role else None,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'referral_code': self.referral_code,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
