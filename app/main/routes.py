from flask import request, jsonify
from app.main import bp_main
from app.main.models import User, RideRequest, RideOffer
from  app.auth import bp_auth


@bp_main.route('users',  methods=['POST'])
def create_user():
    data = request.get_json()
    user = User.get_user_by_email(data['email'])
    if user is None:
        user = User(data['email'],data['name'],data['phone'], data['password'])
        user.password = ""
        User.users.append(user)
        message = { 'user': user.__repr__(),
                    'message': 'User Created Successfully'}
        response = jsonify(message)
        response.status_code = 201
        return response
    message = { 'user':'None',
                'message':'User Exists'}
    response = jsonify(message)
    response.status_code = 300
    return response


@bp_main.route('/', methods = ['POST'])
def login():
    data = request.get_json()


@bp_main.route('users/<string:user_email>/rides', methods = ['POST'])
def create_ride_offer(user_email, **kwargs):
    data = request.get_json()
    user = User.get_user_by_email(user_email)
    rideOffer = RideOffer(data['driver_email'], data['ride_date'], data['departure_time'], data['pick_up_point'], data['destination'], data['charges'])
    rideOffer.ride_id = len(RideOffer.rideOffers) + 1
    user.ride_offers.append(rideOffer)
    RideOffer.rideOffers.append(rideOffer)
    message = {'ride_offer':rideOffer.__repr__(),
               'message':'Ride Offer Created Successfully'}
    response = jsonify(message)
    response.status_code = 201
    return response


@bp_main.route('users/rides/<int:ride_id>', methods = ['GET'])
def get_a_ride_offer(ride_id, **kwargs):
    for ride in RideOffer.rideOffers:
        if ride.ride_id == ride_id:
            message = {'ride_offer':ride.__repr__()}
            response = jsonify(message)
            response.status_code = 200
            return response
    message = {'ride_offer': 'None'}
    response = jsonify(message)
    response.status_code = 301
    return response


@bp_main.route('users/rides', methods = ['GET'])
def get_ride_offers():
    message = {}
    count = 1
    for ride in RideOffer.rideOffers:
        message[count] = ride.__repr__()
        count += 1
    response = jsonify(message)
    response.status_code = 200
    return response


@bp_main.route('users/rides/<int:ride_id>/requests', methods = ['POST'])
def request_ride(ride_id, **kwargs):
    data = request.get_json()
    ride = RideOffer.get_ride_by_id(ride_id)
    rideRequest = RideRequest(data['ride_offer_id'], data['user_email'])
    ride.ride_requests.append(rideRequest)
    message = {'request': rideRequest.__repr__()}
    response = jsonify(message)
    response.status_code = 201
    return response