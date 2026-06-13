from flask import request
from flask_restx import Namespace, Resource, fields
from Services.membership_servic import get_all_plans, buy_membership, get_user_membership_status

membership_route = Namespace(
    "membership", 
    description="Manage user memberships and subscriptions", 
    path="/membership"
)

buy_membership_model = membership_route.model(
    "BuyMembership",
    {
        "user_id": fields.Integer(required=True, description="ID of the existing user"),
        "membership_id": fields.Integer(required=True, description="ID of the membership plan to purchase")
    }
)

@membership_route.route("/plans")
class MembershipPlans(Resource):
    def get(self):
        """View all available library membership tiers"""
        return get_all_plans()

@membership_route.route("/subscribe")
class SubscribeMembership(Resource):
    @membership_route.expect(buy_membership_model)
    def post(self):
        """Purchase or upgrade a membership plan for a user"""
        data = request.get_json()
        return buy_membership(data)

@membership_route.route("/status/<int:user_id>")
class UserMembershipStatus(Resource):
    def get(self, user_id):
        """Check the active subscription status details of a specific user"""
        return get_user_membership_status(user_id)