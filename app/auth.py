from flask import Blueprint, render_template, request, redirect, flash, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET' , 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(username) <=2:
            flash('Username must be greater than 2 characters.', category='error')
        elif len(email) < 4 and '@' in email:
            flash('Email must be greater than 4 char and have @.', category='error')
        elif len(password1) < 6:
            flash('Password must be of atleast 6 char', category='error')
        elif password1 != password2 :
            flash('Password didn\'t match.', category='error')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists. Kindly login.', category='error')
            else:
                hash_method = 'pbkdf2'
                new_user = User(username=username, email=email, password=generate_password_hash(password1, method=hash_method))

                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)

                flash('Account created!', category='success')

                return redirect(url_for("routes.index"))
    
    return render_template('register.html', user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if user.password and check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')

                return redirect(url_for("routes.index"))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', category='success')

    return redirect(url_for('auth.login'))