from Modules.books_module import Book  
from Database.database import db
from Utils.Response import error_response, success_response

def create_book(data):
    try:
        if not data.get("title") or not data.get("category"):
            return error_response("Missing required fields: title and category")

        qty = data.get("quantity", 1)

        new_book = Book(
            title=data.get("title"),
            author=data.get("author"),
            category=data.get("category"),
            quantity=qty,
            available_quantity=qty,  
            publishes_year=data.get("publishes_year")
        )

        db.session.add(new_book)
        db.session.commit()
        return success_response("Book added successfully", {"id": new_book.id}, status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response(str(e))


def get_all_books():
    try:
        books = Book.query.all()
        if not books:
            return success_response("No books found", data=[])

        book_list = []
        for book in books:
            book_list.append({
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "quantity": book.quantity,
                "available_quantity": book.available_quantity,
                "publishes_year": book.publishes_year
            })
        return success_response("Books fetched successfully", book_list)
    except Exception as e:
        return error_response(str(e))


def get_book_by_id(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return error_response(f"Book with id {book_id} not found", status_code=404)

        book_data = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "category": book.category,
            "quantity": book.quantity,
            "available_quantity": book.available_quantity,
            "publishes_year": book.publishes_year
        }
        return success_response("Book found successfully", book_data)
    except Exception as e:
        return error_response(str(e))


def update_book(book_id, data):
    try:
        book = Book.query.get(book_id)
        if not book:
            return error_response(f"Book with id {book_id} not found", status_code=404)

        if "quantity" in data:
            diff = data["quantity"] - book.quantity
            book.quantity = data["quantity"]
            book.available_quantity += diff

        if "title" in data: book.title = data["title"]
        if "author" in data: book.author = data["author"]
        if "category" in data: book.category = data["category"]
        if "publishes_year" in data: book.publishes_year = data["publishes_year"]

        db.session.commit()
        return success_response("Book updated successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(str(e))


def delete_book(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return error_response(f"Book with id {book_id} not found", status_code=404)

        db.session.delete(book)
        db.session.commit()
        return success_response("Book deleted successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(str(e))


def search_books(title=None, author=None, category=None):
    try:
        
        query = Book.query

        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        if category:
            query = query.filter(Book.category.ilike(f"%{category}%"))

        results = query.all()
        
        if not results:
            return success_response("No books matched the search criteria", data=[])

        matched_books = []
        for book in results:
            matched_books.append({
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "quantity": book.quantity,
                "available_quantity": book.available_quantity,
                "publishes_year": book.publishes_year
            })

        return success_response("Search operations completed successfully", matched_books)
    except Exception as e:
        return error_response(str(e))