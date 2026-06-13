from Modules.books_module import Book
from Database.database import db
from Utils.Response import error_response, success_response

def create_book(data):

    try:
        pass
    except Exception as e:
        return error_response(str(e))