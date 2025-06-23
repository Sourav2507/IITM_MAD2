from flask import Blueprint, render_template, redirect, url_for, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from models.customers import *

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            if session['role'] == 'admin':
                return redirect(url_for('admin.admin_db'))
            else:
                return redirect(url_for('user.user_db'))
        else:
            return render_template("login.html")

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                session.permanent = True  # <-- Added here
                session['role'] = user.role
                session['username'] = user.username
                session['email'] = user.email
                if user.role == 'admin':
                    return redirect(url_for('admin.admin_db'))
                return redirect(url_for('user.user_db'))
            return "Wrong Password"
        return "Username Doesn't exist"


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('auth.login'))
        return render_template("register.html")

    elif request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            return redirect(url_for('auth.login'))
        
        password = request.form.get('password')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        phone = request.form.get('ph_no')
        age = request.form.get('age')
        gender = request.form.get('gender')
        reg_no = request.form.get('reg_no')
        address = request.form.get('city') + "," + request.form.get('state')

        user = User(username=username, password=generate_password_hash(password), fname=fname,
                    lname=lname, email=email, phone=phone, age=age, gender=gender,
                    reg_no=reg_no, address=address)
        db.session.add(user)
        db.session.commit()

        session.permanent = True  # <-- Added here
        session['username'] = username
        session['role'] = 'user'
        session['email'] = email

        return redirect(url_for('user.user_db'))


@auth.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')
