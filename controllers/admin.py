from flask import Blueprint,render_template,redirect,url_for,session,request

admin = Blueprint('admin', __name__)

@admin.route('/admin/dashboard')
def admin_db():
    if 'role' in session:
        if session['role']=='admin':
            return render_template('admin_db.html')
    return redirect(url_for('auth.login'))

@admin.route('/admin/manage_slots')
def manage_slots():
    if 'role' in session:
        if session['role']=='admin':
            return render_template('manage_slots.html')
    return redirect(url_for('auth.login'))

@admin.route("/admin/manage_users")
def manage_users():
    if 'role' in session:
        if session['role']=='admin':
            return render_template('manage_users.html')
    return redirect(url_for('auth.login'))

@admin.route('/admin/bookings')
def admin_bookings():
    if 'role' in session:
        if session['role']=='admin':
            return render_template('admin_bookings.html')
    return redirect(url_for('auth.login'))

@admin.route('/admin/add_slot')
def add_slot():
    if 'role' in session:
        if session['role']=='admin':
            return render_template('add_slot.html')
    return redirect(url_for('auth.login'))

@admin.route('/admin/reports')
def reports():
    if 'role' in session:
        if session['role']=='admin':
            return render_template('reports.html')
    return redirect(url_for('auth.login'))