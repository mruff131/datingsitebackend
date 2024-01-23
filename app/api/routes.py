from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema, user_schema

api = Blueprint('api', __name__, url_prefix='/api')


# create cars
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):    #reference in models
    car_make = request.json['make']
    car_model = request.json['model']
    car_year = request.json['year']
    car_color = request.json['color']
    car_vin = request.json['vin']
    user_token = current_user_token.token

    print(f'TESTER:  {current_user_token.token}')

    new_car = Car(car_make, car_model, car_year, car_color, car_vin, user_token=user_token)

    db.session.add(new_car)
    db.session.commit()

    response = car_schema.dump(new_car)
    return jsonify(response)

# retrieve all cars
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# retrieve single car
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car.query.get(id) #retrieving from data base
    response = car_schema.dump(car) #pulling it out
    return jsonify(response)

#update car info
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car (current_user_token, id):
    car = Car.query.get(id)
    car.car_make = request.json['make']
    car.car_model = request.json['model']
    car.car_year = request.json['year']
    car.car_color = request.json['color']
    car.car_vin = request.json['vin']

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

#delete car
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

#delete user
@api.route('/user/<id>', methods = ['DELETE'])
@token_required
def delete_duplicate_user(current_user_token, id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    response = user_schema.dump(user)
    return jsonify(response)

