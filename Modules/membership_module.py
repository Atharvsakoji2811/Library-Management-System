from Database.database import db
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class Membership(db.Model):
    __tablename__ = "memberships"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tier_name = db.Column(db.String(50), nullable=False, unique=True)

    max_books_allowed = db.Column(db.Integer, default=3, nullable=False)
    borrow_duration_days = db.Column(db.Integer, default=14, nullable=False)
    fine_discount_percentage = db.Column(db.Float, default=0.0)

    price = db.Column(db.Float, default=0.0, nullable=False)
    duration_months = db.Column(db.Integer, default=12, nullable=False)

    subscriptions = db.relationship("UserMembership", backref="plan_details", lazy=True)


class UserMembership(db.Model):
    __tablename__ = "user_memberships"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    membership_id = db.Column(
        db.Integer, db.ForeignKey("memberships.id"), nullable=False
    )

    start_date = db.Column(db.Date, nullable=False, default=date.today)
    end_date = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(20), default="active")

    user = db.relationship("User", backref="active_subscription", uselist=False)
