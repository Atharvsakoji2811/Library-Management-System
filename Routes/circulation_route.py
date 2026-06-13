from flask import request
from flask_restx import Namespace, Resource, fields
from Services.circulation_service import issue_book, return_book, get_user_history
from Utils.Check_role import authorize_access

circulation_route = Namespace(
    "circulation", 
    description="books circulation", 
    path="/circulation"
)

issue_model = circulation_route.model(
    "IssueBook",
    {
        "member_id": fields.Integer(required=True, description="ID of the user borrowing the book"),
        "book_id": fields.Integer(required=True, description="ID of the book being borrowed")
    }
)

@circulation_route.route("/issue")
class IssueBook(Resource):
    @circulation_route.expect(issue_model)
    def post(self):
        """Issue/Borrow a book"""
        data = request.get_json()
        return issue_book(data)

@circulation_route.route("/return/<int:circulation_id>")
class ReturnBook(Resource):
    def put(self, circulation_id):
        """Return a borrowed book by transaction ID"""
        return return_book(circulation_id)

@circulation_route.route("/history/user/<int:user_id>")
class UserHistory(Resource):
    
    @authorize_access(allowed_roles=["admin", "user"], check_ownership=True, id_url_param_name="user_id")
    def get(self, user_id):
        """Get circulation history for a specific user"""
        return get_user_history(user_id)