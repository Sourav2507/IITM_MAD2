from models import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(15),nullable=False)
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(25))
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    role = db.Column(db.String(20), default='user',nullable=False)
    phone = db.Column(db.String(10))
    reg_no = db.Column(db.String(15))
    address = db.Column(db.String(20))