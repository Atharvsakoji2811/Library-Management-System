from Database.database import db
from datetime import date

class Book(db.Model):
    __tablename__="books"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100))
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    available_quantity = db.Column(db.Integer, default=0)
    publishes_year = db.Column(db.Integer, nullable=True)

    circulation = db.relationship(
                    "Circulation",
                    backref="book",
                    lazy=True 
                    )