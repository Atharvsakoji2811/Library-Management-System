from flask import request
from flask_restx import Namespace, Resource, fields
from Services.auth_service import register_user, login_user

auth_route = Namespace("auth", description="Authentication operations", path="/auth")

# Registration Payload Model
register_model = auth_route.model(
    "RegisterInput",
    {
        "name": fields.String(required=True, description="Full Name"),
        "email": fields.String(required=True, description="Email address"),
        "password": fields.String(required=True, description="Password"),
        "phone_no": fields.String(required=True, description="Phone number"),
        "address": fields.String(required=True, description="Postal address"),
        "role": fields.String(description="Role (defaults to 'user')")
    }
)

# Login Payload Model
login_model = auth_route.model(
    "LoginInput",
    {
        "email": fields.String(required=True, description="Registered email address"),
        "password": fields.String(required=True, description="Password")
    }
)

@auth_route.route("/register")
class Register(Resource):
    
    @auth_route.expect(register_model)
    def post(self):
        data = request.get_json()
        return register_user(data)

@auth_route.route("/login")
class Login(Resource):
    
    @auth_route.expect(login_model)
    def post(self):
        data = request.get_json()
        return login_user(data)