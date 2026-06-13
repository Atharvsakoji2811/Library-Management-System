from flask import Flask
from flask_restx import Api
from Database.database import db
import os
from dotenv import load_dotenv
from config import config


from Modules.books_module import Book
from Modules.circulation_module import Circulation
from Modules.users_module import User

from Routes.book_route import book_route
from Routes.circulation_route import circulation_route
from Routes.user_route import user_route



load_dotenv()

app =Flask(__name__)

# Configuration
app.config.from_object(config)
db.init_app(app)

with app.app_context():
    db.create_all()

app.secret_key = os.getenv("secret_key")

@app.route("/")
def home():
    return "Hello, world"

api = Api(
    app,
    title="Library Management API",
    doc="/swagger"
)

api.add_namespace(user_route)
api.add_namespace(book_route)
api.add_namespace(circulation_route)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )