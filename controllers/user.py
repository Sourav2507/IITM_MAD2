from flask import Blueprint,render_template,redirect,url_for,session

user = Blueprint('user', __name__)

@user.route('/user')
def user_db():
    return render_template('customer_db.html')
