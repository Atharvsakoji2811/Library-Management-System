from Database.database import db
from Modules.users_module import User
from Utils.Response import error_response, success_response


def create_user(data):

    try:
        users = User.query.all()

        if not users:
            return error_response("Users not found")

        data = []
        for user in users:
            data.append({"id": user.user_id, "name": user.name, "contact": user.email})

        return success_response("User's", data)

    except Exception as e:
        return error_response(str(e))
