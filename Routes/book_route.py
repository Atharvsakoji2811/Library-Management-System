from flask import request
from flask_restx import Namespace, Resource, fields

book_route = Namespace("books", description="manage books", path="/books")


book_model = book_route.model(
    "AddBoook",
    {
        "title": fields.String(description="Book title"),
        "author": fields.String(description="Author name"),
        "category": fields.String(description="Book category"),
        "quantity": fields.Integer(description="Available quantity"),
        "publishes_year": fields.Integer(description="publishes year"),
    },
)


@book_route.route("/add_book", methods=["POST"])
class add_book(Resource):

    @book_route.expect(book_model)
    def post(self):
        data = request.get_json()
        return create_book(data)
