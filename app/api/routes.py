from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Profile, user_schema, profile_schema
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__, url_prefix='/api')


# create account
@api.route('/signup', methods = ['POST'])
def create_user():    #reference in models
    email = request.json['email']
    password = request.json['password']
    new_user = User(email, password)
    user_token = new_user.token

    db.session.add(new_user)
    db.session.commit()

    response = user_schema.dump(new_user)
    return jsonify(response)

# login to account
@api.route('/login', methods=['POST'])
def loginUser():
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    print(email, password)
    try:
        user = User.query.filter_by(email= email).first()
        print(user)
        token = user.token
    except AttributeError:
        return jsonify({"error":"Wrong email or password"}), 401

    
    if not check_password_hash(user.password, password):  #if password incorrect
        return jsonify({"error":"Wrong password"}), 401
    
    return jsonify({
        "access_token" : token,
        "email": email, 
        "passwordHash": password
        ,
}),201




# create profile info
@api.route('/settings', methods=['POST'])
@token_required
def create_profile(current_user_token):
    full_name = request.json.get('fullName')
    phone_number = request.json.get('phoneNumber')
    email_address = request.json.get('emailAddress')
    username = request.json.get('Username')
    bio = request.json.get('bio')
    the_token = current_user_token.token


    print(f'TESTER:  {the_token}')
    print(f'TESTER2:  {current_user_token.token}')

    new_profile = Profile(full_name, phone_number, email_address,username, bio, user_token = the_token )
    db.session.add(new_profile)
    db.session.commit()

    response = profile_schema.dump(new_profile)
    return jsonify(response)


#update account info
@api.route('/settings/<id>', methods = ['POST', 'PUT'])
@token_required
def update_account (current_user_token, id):
    print(f"user id is....{id}")
    user = Profile.query.get(id)
    user.full_name = request.json['full_name']
    user.phone_number = request.json['phone_number']
    user.email_address = request.json['email_address']
    user.username = request.json['username']
    user.bio = request.json['bio']

    db.session.commit()
    response = profile_schema.dump(user)
    return jsonify(response)


@api.route('/settings-profile', methods=['POST', 'PUT'])
@token_required
def update_or_create_account(current_user_token):
    try:
        # Check if the user already has a profile
        user_profile = Profile.query.filter_by(user_token = current_user_token.token).first() 
        print(f'user_profile is {user_profile}')
        
     
        
        if user_profile is not None:
            # Update existing profile
            profile_id = user_profile.profile_id
            print(profile_id)
            print("profile id is not none")
            user = Profile.query.get(profile_id)
            user.full_name = request.json['full_name']
            user.phone_number = request.json['phone_number']
            user.email_address = request.json['email_address']
            user.username = request.json['username']
            user.bio = request.json['bio']

            db.session.commit()
            response = profile_schema.dump(user)
            return jsonify(response)
        else:
            #create_profile
            full_name = request.json.get('full_name')
            phone_number = request.json.get('phone_number')
            email_address = request.json.get('email_address')
            username = request.json.get('username')
            bio = request.json.get('bio')
            the_token = current_user_token.token


            print(f'TESTER:  {the_token}')
            print(f'TESTER2:  {current_user_token.token}')
            print(full_name, phone_number, email_address,username, bio, the_token)

            new_profile = Profile(full_name, phone_number, email_address,username, bio, user_token = the_token )
            db.session.add(new_profile)
            db.session.commit()

            response = profile_schema.dump(new_profile)
            return jsonify(response)

    except Exception as e:
        return jsonify({'message': str(e)}), 500  # Internal server error









# Get user profile info using PROFILE Id
@api.route('/settings/<id>', methods=['GET'])
@token_required
def get_user(current_user_token, id):
    # Retrieve user profile info using PROFILE Id
    user_profile = Profile.query.get(id)
    if user_profile:
        response = profile_schema.dump(user_profile)
        return jsonify(response), 200
    else:
        return jsonify({'message': 'User profile not found'}), 404




# Delete account and profile 
@api.route('/settings', methods=['DELETE'])  
# @api.route('/settings', methods=['DELETE'])  # For profiles without ID
@token_required
def delete_account(current_user_token):

    try:
        # Check if the user has a profile
        try:
            user_profile = Profile.query.filter_by(user_token = current_user_token.token).first() 
            print(f'user_profile is {user_profile}')

            profile_id = user_profile.profile_id # must delete using primary key
            profile = Profile.query.get(profile_id)
            db.session.delete(profile)
            profile_data = profile_schema.dump(profile)
        except:
            profile_data = None
        
        
        if current_user_token is not None:
            user_info = User.query.filter_by(token=current_user_token.token).first()
            user_id = user_info.id
            user = User.query.get(user_id)

            db.session.delete(user)
            db.session.commit()
        
            user_data = user_schema.dump(user)
        else:
            user_data = "check ur token"
        
        return jsonify({'message': 'Account and profile deleted successfully', 
                        'profile': profile_data, 
                        'user': user_data}), 200
    except Exception as e:
            return jsonify({'message': str(e)}), 500  # Internal server error







# # Delete account and profile 
# @api.route('/settings', methods=['DELETE'])  
# # @api.route('/settings', methods=['DELETE'])  # For profiles without ID
# @token_required
# def delete_account(current_user_token, id):
#      #TODO HANDLE IF USER DOES NOT HAVE PROFILE
#     token = current_user_token.token
#     print(token)

#     user = User.query.filter_by(token=token).first()
#     print(user)
#     profile = Profile.query.get(id)  # can only use .get to grab primary key
#     # profile = Profile.query.filter_by(user_token=user.token).first()

#     if profile:
#         db.session.delete(profile)
#     db.session.delete(user)
#     db.session.commit()
#     response = profile_schema.dump(profile)
#     return jsonify(response)
 

#  # Delete Account only (when theres no profile ID)
# @api.route('/account/<id>', methods = ['DELETE'])
# @token_required
# def delete_account_only(current_user_token, id):
#     user = User.query.get(id)
#     db.session.delete(user)
#     db.session.commit()
#     response = profile_schema.dump(user)

#     return jsonify(response)

