from flask import Blueprint,render_template,redirect,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from models.customers import *

user = Blueprint('user', __name__)

@user.route('/user/dashboard')
def user_db():
    print(session)
    user = User.query.filter_by(username=session['username']).first()
    return render_template('customer_db.html')

@user.route('/user/find_parking')
def find_parking():
    return render_template('find_parking.html')

@user.route('/user/bookings')
def bookings():
    return render_template('bookings.html')

@user.route('/user/payments')
def payments():
    return render_template('payments.html')

@user.route('/user/help_and_support')
def help_and_support():
    return render_template('help_and_support.html')

@user.route('/user/notifications')
def notifications():
    return render_template('notifications.html')

@user.route('/user/profile')
def profile():
    return render_template('profile.html')

