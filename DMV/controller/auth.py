from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models import User
from ..import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth",__name__)

@auth.route('/login', methods =['GET','POST'])
def login():
    #If POST request received it takes all data from form and checks against data in db
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password1')
        
        user = User.query.filter_by(email=email).first()
        #checking Users data
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category = 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.practice'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist.',category = True)
        
    return render_template("login.html", user = current_user)


@auth.route('/registration', methods =['GET','POST'])
def registration():
    #If POST request received it takes all data from form and sets to user and saves in db
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        
        #filtering out users inputs
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category = 'error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category = 'error')
        elif password1 != password2:
            flash('Passwords do not match.', category = 'error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category = 'error')
        else:
            #saving USER
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created and logged in successfully!", category="success")
            return redirect(url_for('views.practice'))
    return render_template("registration.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
