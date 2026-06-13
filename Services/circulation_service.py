from Database.database import db
from Modules.circulation_module import Circulation
from Modules.books_module import Book
from Modules.users_module import User
from Utils.Response import error_response, success_response
from Utils.Check_role import authorize_access
from datetime import date, timedelta

FINE_RATE_PER_DAY = 10.0
BORROW_DURATION_DAYS = 14


def issue_book(data):
    try:
        member_id = data.get("member_id")
        book_id = data.get("book_id")

        if not member_id or not book_id:
            return error_response("Missing required fields: member_id and book_id")

        user = User.query.get(member_id)
        if not user:
            return error_response(
                f"User with ID {member_id} does not exist", status_code=404
            )

        book = Book.query.get(book_id)
        if not book:
            return error_response(
                f"Book with ID {book_id} does not exist", status_code=404
            )

        if book.available_quantity <= 0:
            return error_response(
                f"Book '{book.title}' is currently out of stock", status_code=400
            )

        today = date.today()
        calculated_due_date = today + timedelta(days=BORROW_DURATION_DAYS)

        new_record = Circulation(
            member_id=member_id,
            book_id=book_id,
            issue_date=today,
            due_date=calculated_due_date,
            status="borrowed",
            fine_amount=0.0,
        )

        book.available_quantity -= 1

        db.session.add(new_record)
        db.session.commit()

        return success_response(
            "Book issued successfully",
            {"circulation_id": new_record.id, "due_date": str(calculated_due_date)},
            status_code=201,
        )
    except Exception as e:
        db.session.rollback()
        return error_response(str(e))


def return_book(circulation_id):
    try:
        record = Circulation.query.get(circulation_id)
        if not record:
            return error_response(
                f"Circulation log #{circulation_id} not found", status_code=404
            )

        if record.status == "returned":
            return error_response("This book has already been marked as returned")

        book = Book.query.get(record.book_id)
        if book:
            book.available_quantity += 1

        today = date.today()
        record.return_date = today
        record.status = "returned"

        if today > record.due_date:
            late_days = (today - record.due_date).days
            record.fine_amount = float(late_days * FINE_RATE_PER_DAY)
        else:
            record.fine_amount = 0.0

        db.session.commit()

        return success_response(
            "Book returned safely",
            {
                "circulation_id": record.id,
                "fine_assessed": record.fine_amount,
                "days_overdue": max(0, (today - record.due_date).days),
            },
        )
    except Exception as e:
        db.session.rollback()
        return error_response(str(e))


def get_user_history(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return error_response(f"User with ID {user_id} not found", status_code=404)

        logs = Circulation.query.filter_by(member_id=user_id).all()
        if not logs:
            return success_response(
                f"No borrowing history found for user #{user_id}", data=[]
            )

        history_list = []
        for log in logs:
            book = Book.query.get(log.book_id)
            history_list.append(
                {
                    "circulation_id": log.id,
                    "book_id": log.book_id,
                    "book_title": book.title if book else "Unknown Book",
                    "issue_date": str(log.issue_date),
                    "due_date": str(log.due_date),
                    "return_date": str(log.return_date) if log.return_date else None,
                    "fine_amount": log.fine_amount,
                    "status": log.status,
                }
            )

        return success_response(
            f"History for user #{user_id} fetched successfully", history_list
        )
    except Exception as e:
        return error_response(str(e))
