from Database.database import db
from Modules.users_module import User
from Utils.Response import error_response, success_response
from werkzeug.security import generate_password_hash


def create_user(data):
    try:
        if not data.get("name") or not data.get("password"):
            return error_response("Missing required fields: name and password")

        new_user = User(
            name=data.get("name"),
            password=generate_password_hash(data.get("password")),
            phone_no=data.get("phone_no", ""),
            address=data.get("address", ""),
            role=data.get("role", "user"),
            email=data.get("email", ""),
        )

        db.session.add(new_user)
        db.session.commit()

        return success_response(
            "User created successfully", {"id": new_user.id}, status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(str(e))


def get_all_users():
    try:
        users = User.query.all()
        if not users:
            return success_response("No users found", data=[])

        user_list = []
        for user in users:
            user_list.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "phone_no": user.phone_no,
                    "address": user.address,
                    "role": user.role,
                }
            )

        return success_response("Users fetched successfully", user_list)
    except Exception as e:
        return error_response(str(e))


def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return error_response(f"User with id {user_id} not found", status_code=404)

        user_data = {
            "id": user.id,
            "name": user.name,
            "phone_no": user.phone_no,
            "address": user.address,
            "role": user.role,
        }
        return success_response("User found successfully", user_data)
    except Exception as e:
        return error_response(str(e))


def update_user(user_id, data):
    try:
        user = User.query.get(user_id)
        if not user:
            return error_response(f"User with id {user_id} not found", status_code=404)

        if "name" in data:
            user.name = data["name"]
        if "password" in data:
            user.password = data["password"]
        if "phone_no" in data:
            user.phone_no = data["phone_no"]
        if "address" in data:
            user.address = data["address"]
        if "role" in data:
            user.role = data["role"]

        db.session.commit()
        return success_response("User updated successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(str(e))


def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return error_response(f"User with id {user_id} not found", status_code=404)

        db.session.delete(user)
        db.session.commit()
        return success_response("User deleted successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(str(e))
