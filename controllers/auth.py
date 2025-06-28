from flask import Blueprint, render_template, redirect, url_for, session, request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.customers import *
from models.parking import *


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
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data received"}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"message": "Username and password required"}), 400

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                session.permanent = True
                session['role'] = user.role
                session['username'] = user.username
                session['email'] = user.email

                # Correct route based on role
                if user.role == 'admin':
                    redirect_url = url_for('admin.admin_db')
                else:
                    redirect_url = url_for('user.user_db')

                return jsonify({
                    "message": "Login successful",
                    "redirect": redirect_url,
                    "role": user.role
                }), 200
            else:
                return jsonify({"message": "Wrong password"}), 401
        else:
            return jsonify({"message": "Username doesn't exist"}), 404



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

