from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required
import re


# initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///vtu_database.db'
app.config['SECRET_KEY'] = 'FOR ALL THE TIME THAT U SPEND IN MY PARADE!'

# initialize SQLAlchemy
db = SQLAlchemy(app)

# create a User model
from models import Users, Referrals

# initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# load user from user id
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id)) 

# func to validate email
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

# func to validate phone number
def validate_phone_number(phone_number):
    pattern = r'^\+\d{1,3}-\d{1,3}-\d{1,4}-\d{1,4}$'
    return bool(re.match(pattern, phone_number))

# func to validate password
def validate_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(pattern, password))


# six authentication routes 
# 1 pre auth route
@app.route("/")
def auth():
    return render_template("auth/pre_auth.html")

# 2 sign up route
@app.route("/sign-up", methods=['POST', 'GET'])
def sign_up():
    if request.method == 'post':

        # grab the user data
        name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        referral_username = request.form.get("referral_username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # check if username or email already exists
        user = Users.query.filter_by(username=username).first()
        if user:
            flash("Username already exists", category="error")
        user = Users.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category="error")

        # check if name is valid
        if not name.isalpha() or not name.strip():
            flash("Name must contain only alphabetic characters", category="error")
        elif len(name) < 3:
            flash("Name must be at least 3 characters long", category="error")

        # check if username is valid
        if not username.isalnum() or not username.strip():
            flash("Username must contain only alphanumeric characters", category="error")
        elif len(username) < 5:
            flash("Username must be at least 5 characters long", category="error")

        # check if email is valid
        if not validate_email(email):
            flash("Invalid email address", category="error")

        # check if phone number is valid
        if not validate_phone_number(phone_number):
            flash("Invalid phone number format, ", category="error")

        # check if passwords match
        if password1!= password2:
            flash("Passwords do not match", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters long", category="error")
        elif not validate_password(password2):
            flash("Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character", category="error")
        else:
            # checks if referral username exist
            referral = Referrals.query.filter_by(referred_by=referral_username).first()
            if not referral:
                flash("Referral username doesn't exist!", category="error")
                referral_username = None
            else:
                referral_username = referral_username

            # create a new user
            new_user = Users(name=name, username=username, email=email, phone_number=phone_number, referral_username=referral_username)
            new_user.set_password(password1)
            db.session.add(new_user)
            db.session.commit()

            # login the user after signing up
            login_user(new_user)
            return render_template("dashboard.html")
        
    return render_template("auth/sign_up.html")

# 3 login route
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'post':
        # grab the form data 
        username = request.form.get('username')
        password = request.form.get('password')

        # check if user exists
        user = Users.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash('Login successful', category="success")
            login_user(user)
            return render_template("dashboard.html")
        else:
            flash('Invalid username or password', category="error")
    return render_template("auth/login.html")


# logout route (additional route)  
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("auth/pre_auth.html")


# 4 password forgotten route (find account and request otp)
@app.route("/find-account")
def find_account():
    return render_template("auth/find_account.html")

# 5 otp validation route
@app.route("/confirm-otp")
def confirm_otp():
    return render_template("auth/confirm_otp.html")

# 6 changing with new password route
@app.route("/create-new-password")
def create_new_password():
    return render_template("auth/create_new_password.html")


# main routes
# dashboard route
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# runnin' the app 
if __name__ == '__main__':
    app.run(debug=True, port=6000)