from Database.database import db
from Modules.users_module import User
from Utils.Response import error_response, success_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session


def register_user(data):
    try:
        name = data.get("name")
        email = data.get("email")
        password = generate_password_hash(data.get("password"))
        phone_no = data.get("phone_no")
        address = data.get("address")
        role = data.get("role", "user")

        if not all([name, email, password, phone_no, address]):
            return error_response(
                "Missing required fields. Please fill out all fields."
            )

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return error_response(
                "An account with this email already exists", status_code=400
            )

        new_user = User(
            name=name,
            email=email,
            password=password,
            phone_no=phone_no,
            address=address,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return success_response(
            "Registration successful!",
            {"user_id": new_user.id, "email": new_user.email},
            status_code=201,
        )

    except Exception as e:
        db.session.rollback()
        return error_response(str(e))


def login_user(data):
    try:
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return error_response("Email and password are required")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return error_response("Invalid email or password", status_code=401)
        
        session["user_id"] = user.id
        session["role"] = user.role

        user_profile = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }

        return success_response("Login successful!", user_profile)

    except Exception as e:
        return error_response(str(e))
