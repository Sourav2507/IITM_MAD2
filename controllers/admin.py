from flask import Blueprint,render_template,redirect,url_for,session,request

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def admin_db():
    return render_template('admin_db.html')
