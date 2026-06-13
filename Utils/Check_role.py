from Utils.Response import error_response
from functools import wraps
from flask import session, request

def authorize_access(allowed_roles, check_ownership=False, id_url_param_name="user_id"):
    """
    allowed_roles: List of roles allowed (e.g., ['admin', 'librarian', 'user'])
    check_ownership: If True, ensures a 'user' can only access their own resource ID
    id_url_param_name: The name of the ID variable inside the route function arguments
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            
            session_role = session.get("role")
            session_user_id = session.get("user_id")

            if not session_role or not session_user_id:
                return error_response("Unauthorized user. Please log in.", 401)

            if session_role not in allowed_roles:
                return error_response("Access forbidden: Insufficient permissions", 403)

            if session_role == "user" and check_ownership:
                requested_resource_id = kwargs.get(id_url_param_name)
                
                if requested_resource_id and int(requested_resource_id) != int(session_user_id):
                    return error_response("Access forbidden: You cannot modify or view other users' records", 403)

            return func(*args, **kwargs)
        return wrapper
    return decorator