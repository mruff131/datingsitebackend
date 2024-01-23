from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal
from models import User


def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers: #insomia api
            token = request.headers['x-access-token'].split(' ')[1] # bearer dsjdnsjdsnd
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401
        
        try:
            print("trying")
            current_user_token = User.query.filter_by(token = token).first() #checks database for user with token
            print(token)
            print(current_user_token)

        except:
            owner=User.query.filter_by(token=token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):  # secrets adds an additional layer of protection by preventing timed attacks
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated
            
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):  
            return str(obj)
        return super(JSONEncoder,self).default(obj)
