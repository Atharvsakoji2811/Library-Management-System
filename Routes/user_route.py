from flask import request
from flask_restx import Namespace, fields, Resource
from Utils.Check_role import authorize_access
from Services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
)

user_route = Namespace("users", description="manage users", path="/users")

user_model = user_route.model(
    "User",
    {
        "name": fields.String(required=True, description="User name"),
        "password": fields.String(required=True, description="Password"),
        "phone_no": fields.String(required=True, description="Phone number"),
        "address": fields.String(required=True, description="Address"),
        "role": fields.String(description="Role (default: user)"),
        "email": fields.String(required=True, description="User email"),
    },
)


@user_route.route("/add_user")
class AddUser(Resource):

    @authorize_access(allowed_roles=["admin"])
    @user_route.expect(user_model)
    def post(self):
        data = request.get_json()
        return create_user(data)

@user_route.route("/all_users")
class GetAllUsers(Resource):
    def get(self):
        return get_all_users()

@user_route.route("/<int:user_id>")
class UserOperations(Resource):
    def get(self, user_id):
        """Find a user by id"""
        return get_user_by_id(user_id)

    @authorize_access(allowed_roles=["admin"])
    @user_route.expect(user_model, validate=False)
    def put(self, user_id):
        """Update existing user by id"""
        data = request.get_json()
        return update_user(user_id, data)

    @authorize_access(allowed_roles=["admin"])
    def delete(self, user_id):
        """Delete a user by id"""
        return delete_user(user_id)
