from datetime import datetime, timedelta
from enum import Enum
import uuid
from app import db

class UserRole(Enum):
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"
    DEVELOPER = "developer"
    CONTENT_CREATOR = "content_creator"
    MARKETER = "marketer"
    INVESTOR = "investor"
    ADMIN = "admin"

class SubscriptionTier(Enum):
    # Student/Parent tiers
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    FAMILY = "family"
    
    # Developer tiers
    DEVELOPER_STARTER = "developer_starter"
    DEVELOPER_PROFESSIONAL = "developer_professional"
    DEVELOPER_ENTERPRISE = "developer_enterprise"
    
    # Teacher tiers
    TEACHER_INDIVIDUAL = "teacher_individual"
    TEACHER_ADVANCED = "teacher_advanced"
    SCHOOL_INSTITUTION = "school_institution"
    
    # Content Creator tiers
    CREATOR_STARTER = "creator_starter"
    CREATOR_PROFESSIONAL = "creator_professional"
    CONTENT_STUDIO = "content_studio"
    
    # Marketer tiers
    AFFILIATE_MARKETER = "affiliate_marketer"
    MARKETING_PARTNER = "marketing_partner"
    MARKETING_AGENCY = "marketing_agency"
    
    # Investor tiers
    ANGEL_INVESTOR = "angel_investor"
    INSTITUTIONAL_INVESTOR = "institutional_investor"
    VC_FUND = "vc_fund"
    
    # Early Customer tiers
    EARLY_INDIVIDUAL = "early_individual"
    EARLY_FAMILY = "early_family"
    PIONEER_SCHOOL = "pioneer_school"

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"

class LoyaltyLevel(Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"

class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    tier = db.Column(db.Enum(SubscriptionTier), nullable=False, unique=True)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    price_monthly = db.Column(db.Float, default=0.0)
    price_quarterly = db.Column(db.Float, default=0.0)
    price_yearly = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(3), default='DZD')
    
    # Features and limits
    max_students = db.Column(db.Integer, default=0)  # 0 = unlimited
    max_classes = db.Column(db.Integer, default=0)
    max_content_uploads = db.Column(db.Integer, default=0)
    api_calls_per_day = db.Column(db.Integer, default=0)
    storage_gb = db.Column(db.Float, default=1.0)
    
    # Permissions
    can_create_content = db.Column(db.Boolean, default=False)
    can_access_analytics = db.Column(db.Boolean, default=False)
    can_use_api = db.Column(db.Boolean, default=False)
    can_publish_commercially = db.Column(db.Boolean, default=False)
    has_priority_support = db.Column(db.Boolean, default=False)
    
    # Commission rates
    content_commission_rate = db.Column(db.Float, default=0.0)
    referral_commission_rate = db.Column(db.Float, default=0.0)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subscriptions = db.relationship('UserSubscription', backref='plan', lazy=True)

class UserSubscription(db.Model):
    __tablename__ = 'user_subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plans.id'), nullable=False)
    
    # Subscription details
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    auto_renew = db.Column(db.Boolean, default=True)
    
    # Billing
    billing_cycle = db.Column(db.String(20), default='monthly')  # monthly, quarterly, yearly
    next_billing_date = db.Column(db.DateTime)
    
    # Usage tracking
    current_students = db.Column(db.Integer, default=0)
    current_classes = db.Column(db.Integer, default=0)
    current_content_uploads = db.Column(db.Integer, default=0)
    api_calls_today = db.Column(db.Integer, default=0)
    storage_used_gb = db.Column(db.Float, default=0.0)
    
    # Discounts and promotions
    discount_percentage = db.Column(db.Float, default=0.0)
    promotion_code = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payments = db.relationship('Payment', backref='subscription', lazy=True)

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('user_subscriptions.id'), nullable=False)
    
    # Payment details
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='DZD')
    payment_method = db.Column(db.String(50))  # credit_card, bank_transfer, mobile_payment
    transaction_id = db.Column(db.String(100), unique=True)
    
    # Status and dates
    status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime, nullable=False)
    
    # Additional info
    description = db.Column(db.String(200))
    invoice_number = db.Column(db.String(50), unique=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BravolinoPoints(db.Model):
    __tablename__ = 'bravolino_points'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Points balance
    total_points = db.Column(db.Integer, default=0)
    available_points = db.Column(db.Integer, default=0)
    used_points = db.Column(db.Integer, default=0)
    
    # Loyalty level
    loyalty_level = db.Column(db.Enum(LoyaltyLevel), default=LoyaltyLevel.BRONZE)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('PointTransaction', backref='user_points', lazy=True)

class PointTransaction(db.Model):
    __tablename__ = 'point_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_points_id = db.Column(db.Integer, db.ForeignKey('bravolino_points.id'), nullable=False)
    
    # Transaction details
    points = db.Column(db.Integer, nullable=False)  # positive for earning, negative for spending
    transaction_type = db.Column(db.String(50), nullable=False)  # subscription, referral, purchase, etc.
    description = db.Column(db.String(200))
    reference_id = db.Column(db.String(100))  # reference to related record
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Referral(db.Model):
    __tablename__ = 'referrals'
    
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Referral details
    referral_code = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    
    # Commission
    commission_rate = db.Column(db.Float, default=0.15)
    commission_earned = db.Column(db.Float, default=0.0)
    commission_paid = db.Column(db.Boolean, default=False)
    
    # Dates
    referred_date = db.Column(db.DateTime, default=datetime.utcnow)
    completed_date = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Investment(db.Model):
    __tablename__ = 'investments'
    
    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Investment details
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='DZD')
    investment_type = db.Column(db.String(50))  # angel, institutional, vc
    equity_percentage = db.Column(db.Float)
    
    # Status and dates
    status = db.Column(db.String(20), default='pending')  # pending, approved, completed, cancelled
    investment_date = db.Column(db.DateTime)
    maturity_date = db.Column(db.DateTime)
    
    # Returns
    expected_return_rate = db.Column(db.Float)
    actual_return_rate = db.Column(db.Float)
    
    # Legal
    contract_signed = db.Column(db.Boolean, default=False)
    due_diligence_completed = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UsageLimit(db.Model):
    __tablename__ = 'usage_limits'
    
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('user_subscriptions.id'), nullable=False)
    
    # Daily limits
    api_calls_limit = db.Column(db.Integer, default=0)
    api_calls_used = db.Column(db.Integer, default=0)
    last_api_reset = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Monthly limits
    content_uploads_limit = db.Column(db.Integer, default=0)
    content_uploads_used = db.Column(db.Integer, default=0)
    last_content_reset = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Storage limits
    storage_limit_gb = db.Column(db.Float, default=1.0)
    storage_used_gb = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Helper functions
def generate_referral_code():
    """Generate a unique referral code"""
    return str(uuid.uuid4())[:8].upper()

def calculate_loyalty_level(total_points):
    """Calculate loyalty level based on total points"""
    if total_points >= 15000:
        return LoyaltyLevel.PLATINUM
    elif total_points >= 5000:
        return LoyaltyLevel.GOLD
    elif total_points >= 1000:
        return LoyaltyLevel.SILVER
    else:
        return LoyaltyLevel.BRONZE

def get_plan_by_tier(tier):
    """Get subscription plan by tier"""
    return SubscriptionPlan.query.filter_by(tier=tier, is_active=True).first()

def check_usage_limits(subscription_id, limit_type):
    """Check if user has exceeded usage limits"""
    usage = UsageLimit.query.filter_by(subscription_id=subscription_id).first()
    if not usage:
        return True
    
    if limit_type == 'api_calls':
        # Reset daily limits if needed
        if usage.last_api_reset.date() < datetime.utcnow().date():
            usage.api_calls_used = 0
            usage.last_api_reset = datetime.utcnow()
            db.session.commit()
        return usage.api_calls_used < usage.api_calls_limit
    
    elif limit_type == 'content_uploads':
        # Reset monthly limits if needed
        if usage.last_content_reset.month != datetime.utcnow().month:
            usage.content_uploads_used = 0
            usage.last_content_reset = datetime.utcnow()
            db.session.commit()
        return usage.content_uploads_used < usage.content_uploads_limit
    
    elif limit_type == 'storage':
        return usage.storage_used_gb < usage.storage_limit_gb
    
    return False

