from flask import Blueprint,render_template,redirect,url_for,session,jsonify,request,current_app
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import os
from models.customers import *
from models.parking import *

user = Blueprint('user', __name__)

@user.route('/user/dashboard')
def user_db():
    print(session)
    user = User.query.filter_by(username=session['username']).first()
    return render_template('customer_db.html')

@user.route('/user/find_parking')
def find_parking():
    return render_template('find_parking.html')

@user.route('/user/find_parking_data')
def find_parking_data():
    parking_lots = ParkingLot.query.all()
    result = []
    for lot in parking_lots:
        result.append({
            'id': lot.id,
            'name': lot.name,
            'address': lot.address,
            'available': lot.capacity-lot.occupied,
            'price': lot.price,
            'date_of_registration': lot.date_of_registration.strftime('%Y-%m-%d')
        })
    return jsonify(result)


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

# @user.route('/user/<id>')
# def user_by_id(id):
#     print("User ID requested:", id)
#     print("User ID requested:", id)
#     import traceback
#     traceback.print_stack()
#     return redirect(url_for('auth.login'))

@user.route('/user/profile')
def profile():
    return render_template('profile.html')

@user.route("/user/data", methods=["GET", "POST"])
def handle_user_data():
    username = session.get("username")
    if not username:
        return jsonify(error="Unauthorized"), 401

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(error="User not found"), 404

    if request.method == "GET":
        # Return profile data
        return jsonify({
            "fname": user.fname,
            "lname": user.lname,
            "phone": user.phone,
            "age": user.age,
            "gender": user.gender,
            "reg_no": user.reg_no,
            "address": user.address,
            "email": user.email,
            "role": user.role,
            "profile_image": user.profile_image or "/static/images/person.png"
        })

    elif request.method == "POST":
        # Update profile data
        data = request.get_json()

        user.fname = data.get("fname", user.fname)
        user.lname = data.get("lname", user.lname)
        user.phone = data.get("phone", user.phone)
        user.age = data.get("age", user.age)
        user.reg_no = data.get("reg_no", user.reg_no)
        user.address = data.get("address", user.address)

        db.session.commit()
        return jsonify(message="Profile updated successfully.")

@user.route('/user/upload-image', methods=['POST'])
def upload_image():
    username = session.get("username")
    if not username:
        return jsonify({"error": "Not logged in"}), 401

    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(f"{username}.png")
    folder_path = os.path.join("static", "images")  # 🟢 Fix here

    # ✅ Create directory if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filepath = os.path.join(folder_path, filename)
    file.save(filepath)

    # Update database path (relative)
    user = User.query.filter_by(username=username).first()
    user.profile_image = f"images/{filename}"  # just the relative path
    db.session.commit()

    return jsonify({
        "message": "Image uploaded successfully.",
        "image_url": f"/images/{filename}"
    })
