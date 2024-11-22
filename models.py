from main import db
from flask_login import UserMixin

# user model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)

    # back relationship -> user (referrer) can have many referrals
    referrals = db.relationship('Referrals', backref='referrer')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.phone_number}') referred: '{self.referrals}'"
    

# referral model
class Referrals(db.Model):
    # relationship -> many users can't refer same single referral
    # but rather one referral must be referred by single user
    referral_id = db.Column(db.Integer, primary_key=True)
    referred_by = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)


    
    def __repr__(self):
        return f"Referral('{self.referred_by}')"



# transaction model
class Transaction(db.Model):
    # transaction_id
    # user_id
    # user_username
    # transaction_type 
    # transaction_sender
    # transaction receiver
    # transaction_cost
    # transaction_date
    # transaction_status
    pass
