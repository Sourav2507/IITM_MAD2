from flask import Flask,Blueprint,render_template,url_for,redirect,session
from controllers.auth import auth
from controllers.admin import admin
from controllers.user import user
from models import db
from flask_migrate import Migrate
from models.customers import *
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)

app.secret_key = "Modern_application_development"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)

@app.route('/')
def home():
    return render_template('landing.html')

def create_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com',password = generate_password_hash('cupcake/mad@007_admin'),role='admin')
        db.session.add(admin)
        db.session.commit()
    return

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True,port=3000)
