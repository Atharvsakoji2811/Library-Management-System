from Database.database import db
from Modules.membership_module import Membership, UserMembership
from Modules.users_module import User 
from Utils.Response import error_response, success_response
from datetime import date, timedelta

def seed_membership_plans_if_empty():
    """Helper function to automatically insert your 4 tiers if they don't exist"""
    if Membership.query.first() is None:
        plans = [
            Membership(tier_name="Weekly", max_books_allowed=2, borrow_duration_days=7, fine_discount_percentage=0.0, price=50.0, duration_months=0), # handled as 7 days
            Membership(tier_name="Silver", max_books_allowed=4, borrow_duration_days=20, fine_discount_percentage=10.0, price=150.0, duration_months=1),
            Membership(tier_name="Gold", max_books_allowed=6, borrow_duration_days=25, fine_discount_percentage=25.0, price=750.0, duration_months=6),
            Membership(tier_name="Platinum", max_books_allowed=10, borrow_duration_days=30, fine_discount_percentage=50.0, price=1200.0, duration_months=12)
        ]
        db.session.add_all(plans)
        db.session.commit()


def get_all_plans():
    try:
        seed_membership_plans_if_empty()
        plans = Membership.query.all()
        
        plan_list = []
        for p in plans:
            plan_list.append({
                "id": p.id,
                "tier_name": p.tier_name,
                "max_books_allowed": p.max_books_allowed,
                "borrow_duration_days": p.borrow_duration_days,
                "fine_discount_percentage": f"{p.fine_discount_percentage}%",
                "price": p.price,
                "duration": f"1 Week" if p.tier_name == "Weekly" else f"{p.duration_months} Month(s)"
            })
        return success_response("Membership plans retrieved successfully", plan_list)
    except Exception as e:
        return error_response(str(e))


def buy_membership(data):
    try:
        seed_membership_plans_if_empty()
        user_id = data.get("user_id")
        membership_id = data.get("membership_id")

        if not user_id or not membership_id:
            return error_response("Missing required fields: user_id and membership_id")

        user = User.query.get(user_id)
        if not user:
            return error_response(f"User with ID {user_id} does not exist. Cannot grant membership.", status_code=404)

        plan = Membership.query.get(membership_id)
        if not plan:
            return error_response("Selected membership tier scheme does not exist.", status_code=404)

        start = date.today()
        if plan.tier_name == "Weekly":
            end = start + timedelta(days=7)
        else:
            end = start + timedelta(days=30 * plan.duration_months)

        existing_active_subs = UserMembership.query.filter_by(user_id=user_id, status="active").all()
        for active_sub in existing_active_subs:
            active_sub.status = "expired"

        new_subscription = UserMembership(
            user_id=user_id,
            membership_id=membership_id,
            start_date=start,
            end_date=end,
            status="active"
        )

        db.session.add(new_subscription)
        db.session.commit()

        return success_response(
            f"Successfully subscribed to {plan.tier_name} plan!",
            {
                "subscription_id": new_subscription.id,
                "tier_name": plan.tier_name,
                "expires_on": str(end)
            },
            status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(str(e))


def get_user_membership_status(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return error_response(f"User with ID {user_id} not found", status_code=404)

        sub = UserMembership.query.filter_by(user_id=user_id, status="active").first()
        
        if not sub:
            return success_response("User is running on the standard basic free tier profile", {
                "tier_name": "Free Tier",
                "max_books_allowed": 3,
                "borrow_duration_days": 14,
                "status": "No Active Subscription Found"
            })

        if date.today() > sub.end_date:
            sub.status = "expired"
            db.session.commit()
            return success_response("Your subscription package has expired.", {"status": "expired"})

        return success_response("Active account tier configuration found", {
            "tier_name": sub.plan_details.tier_name,
            "max_books_allowed": sub.plan_details.max_books_allowed,
            "borrow_duration_days": sub.plan_details.borrow_duration_days,
            "fine_discount": f"{sub.plan_details.fine_discount_percentage}%",
            "start_date": str(sub.start_date),
            "end_date": str(sub.end_date)
        })
    except Exception as e:
        return error_response(str(e))