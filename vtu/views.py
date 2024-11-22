from flask import render_template, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from vtu import db
from vtu.models import Users, Referrals
import re
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)
views = Blueprint('views', __name__)


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
@auth.route("/")
def auth():
    return render_template("auth/pre_auth.html")

# 2 sign up route
@auth.route("/sign-up", methods=['POST', 'GET'])
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
        if password1 != password2:
            flash("Passwords do not match", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters long", category="error")
        elif not validate_password(password2):
            flash \
                ("Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character", category="error")
        else:
            # checks if referral username exist
            referral = Referrals.query.filter_by(referred_by=referral_username).first()
            if not referral:
                flash("Referral username doesn't exist!", category="error")
                referral_username = None
            else:
                referral_username = referral_username

            # create a new user
            new_user = Users(name=name, username=username, email=email, phone_number=phone_number, referral_username=referral_username, password=generate_password_hash(password2))
            new_user.set_password(password1)
            db.session.add(new_user)
            db.session.commit()

            # login the user after signing up
            login_user(new_user)
            return render_template("dashboard.html")

    return render_template("auth/sign_up.html")

# 3 login route
@auth.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'post':
        # grab the form data
        username = request.form.get('username_or_email')
        password = request.form.get('password')

        # check if user exists
        # login with username and password
        user_with_username = Users.query.filter_by(username=username).first()
        if user_with_username and user_with_username.check_password_hash(password):
            flash('Login successful', category="success")
            login_user(user_with_username)
            return render_template("dashboard.html")

        # login with email and password
        elif not user_with_username:
            user_with_email = Users.query.filter_by(email=username).first()
            if user_with_email and user_with_email.check_password_hash(password):
                flash('Login successful', category="success")
                login_user(user_with_email)
                return render_template("dashboard.html")

        else:
            flash('Invalid username or password', category="error")
    return render_template("auth/login.html")


# logout route (additional route)
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("auth/pre_auth.html")


# 4 password forgotten route (find account and request otp)
@auth.route("/find-account")
def find_account():
    return render_template("auth/find_account.html")

# 5 otp validation route
@auth.route("/confirm-otp")
def confirm_otp():
    return render_template("auth/confirm_otp.html")

# 6 changing with new password route
@auth.route("/create-new-password")
def create_new_password():
    return render_template("auth/create_new_password.html")


# main routes
# dashboard route
@views.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
