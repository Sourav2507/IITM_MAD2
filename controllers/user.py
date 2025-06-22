from flask import Blueprint,render_template,redirect,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from models.customers import *

user = Blueprint('user', __name__)

@user.route('/user')
def user_db():
    print(session)
    user = User.query.filter_by(username=session['username']).first()
    return render_template('customer_db.html')

@user.route('/find_parking')
def find_parking():
    return render_template('find_parking.html')

@user.route('/bookings')
def bookings():
    return render_template('find_parking.html')

@user.route('/about')
def about():
    return render_template('find_parking.html')

