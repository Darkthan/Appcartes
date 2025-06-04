from . import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, printer, user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    classe = db.Column(db.String(80))

class CardRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(200))
    classe = db.Column(db.String(80))
    status = db.Column(db.String(20), default='Demande')  # Demande, En cours, Disponible
