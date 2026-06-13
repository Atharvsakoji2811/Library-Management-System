from flask import request
from flask_restx import Namespace, Resource, fields

circulation_route = Namespace(
    "circulation",
    description="books circulation",
    path="/circulation"
)

borrow_book_model = circulation_route.model(
    "borrow_book",{
        "user_id": fields.Integer(required=True),
        "book_id": fields.Integer(required=True)
    }
)