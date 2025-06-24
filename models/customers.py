from models import db
from datetime import datetime

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
    profile_image = db.Column(db.String(200), default='images/person.png')

class Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.Date,nullable = False)
    amount = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String(7),default='unpaid')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(8), nullable=False)
    date_sent = db.Column(db.Date, default=datetime.utcnow)
    heading = db.Column(db.String(50))
    message = db.Column(db.String(250))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    rating = db.Column(db.Integer)  # 1 to 5
    comments = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
