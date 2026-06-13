from flask import request
from flask_restx import Namespace, Resource, fields
from Utils.Check_role import authorize_access
from Services.book_service import (
    create_book,
    get_all_books,
    get_book_by_id,
    update_book,
    delete_book,
    search_books
)

book_route = Namespace("books", description="manage books", path="/books")

book_model = book_route.model(
    "Book",
    {
        "title": fields.String(required=True, description="Book title"),
        "author": fields.String(description="Author name"),
        "category": fields.String(required=True, description="Book category"),
        "quantity": fields.Integer(description="Total quantity"),
        "publishes_year": fields.Integer(description="Publishing year"),
    },
)

@book_route.route("/add_book")
class AddBook(Resource):
    
    @authorize_access(allowed_roles=["admin", "librarian"])
    @book_route.expect(book_model)
    def post(self):
        """Add a new book"""
        data = request.get_json()
        return create_book(data)

@book_route.route("/all_books")
class GetAllBooks(Resource):
    def get(self):
        """Show all books"""
        return get_all_books()

@book_route.route("/<int:book_id>")
class BookOperations(Resource):
    def get(self, book_id):
        """Find a book by id"""
        return get_book_by_id(book_id)

    @authorize_access(allowed_roles=["admin", "librarian"])
    @book_route.expect(book_model, validate=False)
    def put(self, book_id):
        """Update existing book by id"""
        data = request.get_json()
        return update_book(book_id, data)
    
    @authorize_access(allowed_roles=["admin", "librarian"])
    def delete(self, book_id):
        """Delete a book by id"""
        return delete_book(book_id)

@book_route.route("/search")
class SearchBooks(Resource):
    @book_route.doc(params={
        'title': 'Search by book title/name',
        'author': 'Search by author name',
        'category': 'Search by category'
    })
    def get(self):
        """Search books by title, author, or category"""
        title = request.args.get('title')
        author = request.args.get('author')
        category = request.args.get('category')
        
        return search_books(title=title, author=author, category=category)