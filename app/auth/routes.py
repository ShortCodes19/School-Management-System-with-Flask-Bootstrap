from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth_bp
from ..extensions import db
from ..models import User

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if not email or not password or password != confirm:
            flash('Please fill form correctly', 'danger')
            return redirect(url_for('auth.signup'))

        # check existing
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return redirect(url_for('auth.signup'))
        
        new_user = User(first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account Created!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged In Successfully!', 'success')
            return redirect(url_for('views.dashboard'))
        
        flash('Invalid email or password!', 'danger')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')
    

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return render_template('auth/login.html')