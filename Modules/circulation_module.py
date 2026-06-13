from Database.database import db
from datetime import date


class Circulation(db.Model):
    __tablename__ = "circulation"

    id = db.Column(db.Integer, primary_key=True)
    issue_date = db.Column(db.Date, nullable=False, default=date.today)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    fine_amount = db.Column(db.Numeric(10, 2), default=0)
    status = db.Column(db.String(20), default="issued")

    member_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
