from Database.database import db

class User(db.Model):
    __tablename__="user"

    id=db.Column(db.Integer,unique=True,primary_key=True)
    name=db.Column(db.String(250),nullable=False)
    password=db.Column(db.String(250),nullable=False)
    phone_no=db.Column(db.String(250),nullable=False)
    address=db.Column(db.String(250),nullable=False)
    role=db.Column(db.String(250),default="user",)

    circulation = db.relationship(
                    "Circulation",
                    backref="user",
                    lazy=True 
                    )