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





#Booking a Parking lot for customers

@user.route('/user/find_parking')
def find_parking():
    return render_template('find_parking.html')

@user.route('/user/find_parking_data')
def find_parking_data():
    parking_lots = ParkingLot.query.all()
    user_id = session.get('user_id')
    result = []

    for lot in parking_lots:
        has_booked = False
        booking = None

        if user_id:
            booking = Booking.query.filter_by(
                customer_id=user_id,
                parking_lot_id=lot.id
            ).first()

        result.append({
            'id': lot.id,
            'name': lot.name,
            'address': lot.address,
            'capacity': lot.capacity,
            'occupied': lot.occupied,
            'price': lot.price,
            'date_of_registration': lot.date_of_registration.strftime('%Y-%m-%d'),
            'requested': booking is not None,
            'start_time': booking.start_time.isoformat() if booking else None,
            'end_time': booking.end_time.isoformat() if booking else None
        })

    return jsonify(result)


@user.route('/user/book_spot', methods=['POST'])
def book_spot():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    data = request.get_json()
    lot_id = data.get('lot_id')
    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')

    if not lot_id or not start_time_str or not end_time_str:
        return jsonify({'success': False, 'message': 'Missing booking time'}), 400

    try:
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid date format'}), 400

    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({'success': False, 'message': 'Parking lot not found'})

    available = lot.capacity - lot.occupied
    if available <= 0:
        return jsonify({'success': False, 'message': 'No spots available'})

    # Find used slots
    used_slots = db.session.query(Booking.slot_id).filter_by(
        parking_lot_id=lot_id,
        status='Requested'
    ).all()
    used_slot_ids = set(slot[0] for slot in used_slots)

    # Find first available slot
    available_slot = next((i for i in range(1, lot.capacity + 1) if i not in used_slot_ids), None)
    if available_slot is None:
        return jsonify({'success': False, 'message': 'No slots free'})

    # Create new booking
    booking = Booking(
        customer_id=session['user_id'],
        parking_lot_id=lot.id,
        slot_id=available_slot,
        status='Requested',
        date_booked=datetime.utcnow(),
        start_time=start_time,
        end_time=end_time,
    )

    lot.occupied += 1
    db.session.add(booking)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Booking successful', 'slot': available_slot})

@user.route('/user/cancel_booking', methods=['POST'])
def cancel_booking():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.get_json()
    lot_id = data.get('lot_id')

    if not lot_id:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    user_id = session['user_id']

    # Only cancel the active requested booking
    booking = Booking.query.filter_by(
        customer_id=user_id,
        parking_lot_id=lot_id,
        status='Requested'
    ).first()

    if not booking:
        return jsonify({"success": False, "message": "Booking not found"}), 404

    try:
        parking_lot = ParkingLot.query.get(lot_id)
        if parking_lot.occupied > 0:
            parking_lot.occupied -= 1

        db.session.delete(booking)
        db.session.commit()

        return jsonify({"success": True})

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500





@user.route('/user/bookings')
def bookings():
    return render_template('bookings.html')

@user.route('/user/my_bookings')
def my_bookings():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    user_id = session['user_id']
    now = datetime.utcnow()

    bookings = (
        Booking.query
        .filter_by(customer_id=user_id)
        .join(ParkingLot)
        .add_entity(ParkingLot)
        .order_by(Booking.start_time.asc())
        .all()
    )

    upcoming = []
    past = []

    for booking, lot in bookings:
        data = {
            'id': booking.id,
            'location': lot.name,
            'address': lot.address,
            'start_time': booking.start_time.isoformat(),
            'end_time': booking.end_time.isoformat(),
            'status': booking.status
        }
        if booking.end_time >= now:
            upcoming.append(data)
        else:
            past.append(data)

    return jsonify({"success": True, "upcoming": upcoming, "past": past})

@user.route('/user/cancel_existing_booking/<int:booking_id>', methods=['POST'])
def cancel_existing_booking(booking_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    booking = Booking.query.filter_by(id=booking_id, customer_id=session['user_id']).first()

    if not booking:
        return jsonify({'success': False, 'message': 'Booking not found'}), 404

    db.session.delete(booking)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Booking deleted successfully'})




@user.route('/user/payments')
def payments():
    return render_template('payments.html')

@user.route('/user/help_and_support')
def help_and_support():
    return render_template('help_and_support.html')

@user.route('/user/notifications')
def notifications():
    return render_template('notifications.html')



#Profile Section

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
    folder_path = os.path.join("static", "images")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filepath = os.path.join(folder_path, filename)
    file.save(filepath)

    user = User.query.filter_by(username=username).first()
    user.profile_image = f"images/{filename}"
    db.session.commit()

    return jsonify({
        "message": "Image uploaded successfully.",
        "image_url": f"/images/{filename}"
    })
