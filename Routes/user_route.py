from flask import request
from flask_restx import Namespace, fields, Resource

user_route = Namespace("users", description="manage users", path="/users")

user_model = user_route.model(
    "User",
    {
        "user_name": fields.String(description="user name"),
        "user_email": fields.String(description="user email"),
        "password": fields.String(description="password"),
    },
)


@user_route.route("/add_user", methods=["POST"])
class add_user(Resource):

    @user_route.expect(user_model)
    def post(self):
        data = request.get_json()
        return create_user(data)
