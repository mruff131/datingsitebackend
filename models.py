from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets



login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()  #built in sql

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=True, default='')
    token = db.Column(db.String, default='', unique= True)  # make sure u include A foreign key next time

    def __init__(self, email, password='', g_auth_verify=False):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
    
    def set_token(self, length):
        return (secrets.token_hex(length))

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'User {self.email} has been added to the database.'
    
class Profile(db.Model):
    profile_id = db.Column(db.String, primary_key=True)
    full_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(30), nullable=False)  
    email_address = db.Column(db.String(70))
    username = db.Column(db.String(30))   # should be integer for future ref.
    bio = db.Column(db.String(500))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, full_name, phone_number, email_address, username, bio, user_token, profile_id= ''):
        self.profile_id = self.set_id()
        self.full_name = full_name
        self.phone_number = phone_number
        self.email_address = email_address
        self.username = username
        self.bio = bio
        self.user_token = user_token

    def __repr__(self):
        return f'The following profile has been added to the application.'
    
    def set_id(self):
        return (secrets.token_urlsafe())
    
    
    
    
        
class ProfileSchema(ma.Schema):
    class Meta:
        fields = ['profile_id', 'full_name', 'phone_number', 'email_address', 'username', 'bio',]


class UserSchema(ma.Schema):
    class Meta:
        fields = ['id',  'password', 'email', 'token' ]   #this info makes info from class serialized and  puts in json format and displays to user
        


user_schema = UserSchema()
profile_schema = ProfileSchema()
























# car_schema = CarSchema()
# cars_schema = CarSchema(many=True) // More than one

# class Dating(db.Model):
#     profile_id = db.Column(db.String, primary_key=True)
#     image_url = db.Column(db.String(500))
#     profile_info = db.Column(db.String(150), nullable=False)  #the t
#     phone_number = db.Column(db.String(150))
#     email_address = db.Column(db.String(4))   # should be integer for future ref.
#     username = db.Column(db.String(25))
#     user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

#     def __init__(self, full_name, phone_number, email_address, username, bio, user_token, car_id= ''):
#         self.car_id = self.set_id() #next time use plain ID not car_id..will cause errors in react MUI tables
#         self.full_name = full_name
#         self.phone_number = phone_number
#         self.email_address = email_address
#         self.username = username 
#         self.bio = bio
#         self.user_token = user_token

#     def __repr__(self):
#         return f'The following car has been added to the application.'
    
#     def set_id(self):
#         return (secrets.token_urlsafe())
    
        
# class CarSchema(ma.Schema):
#     class Meta:
#         fields = ['car_id', 'full_name', 'phone_number', 'email_address', 'username', 'bio']