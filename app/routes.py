from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User, Student, CardRequest
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask import current_app as app
import csv

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/auth')

@app.route('/')
@login_required
def index():
    return redirect(url_for('request_card'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role != 'admin':
        return 'Unauthorized', 403
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        user = User(username=username, password=generate_password_hash(password), role=role)
        db.session.add(user)
        db.session.commit()
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/admin/import', methods=['POST'])
@login_required
def import_csv():
    if current_user.role != 'admin':
        return 'Unauthorized', 403
    file = request.files['file']
    if file:
        reader = csv.reader(file.stream.read().decode().splitlines())
        for row in reader:
            if len(row) >= 3:
                student = Student(first_name=row[0], last_name=row[1], classe=row[2])
                db.session.add(student)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/students')
@login_required
def students():
    query = request.args.get('q', '')
    results = Student.query.filter(
        (Student.first_name.ilike(f'%{query}%')) | (Student.last_name.ilike(f'%{query}%'))
    ).all()
    suggestions = [f"{s.first_name} {s.last_name} {s.classe}" for s in results]
    return jsonify(suggestions)

@app.route('/request', methods=['GET', 'POST'])
@login_required
def request_card():
    if request.method == 'POST':
        student_name = request.form['student_name']
        classe = request.form['classe']
        cr = CardRequest(student_name=student_name, classe=classe)
        db.session.add(cr)
        db.session.commit()
        flash('Demande enregistree')
        return redirect(url_for('request_card'))
    return render_template('request.html')

@app.route('/printer', methods=['GET', 'POST'])
@login_required
def printer():
    if current_user.role != 'printer' and current_user.role != 'admin':
        return 'Unauthorized', 403
    if request.method == 'POST':
        cr_id = request.form['id']
        status = request.form['status']
        cr = CardRequest.query.get(cr_id)
        if cr:
            cr.status = status
            db.session.commit()
    cards = CardRequest.query.all()
    return render_template('printer.html', cards=cards)

@app.route('/kiosk')
def kiosk():
    cards = CardRequest.query.filter(CardRequest.status.in_(['En cours', 'Disponible'])).all()
    return render_template('kiosk.html', cards=cards)
