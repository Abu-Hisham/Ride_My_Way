from flask import request, jsonify, g
from flask_httpauth import HTTPBasicAuth
from app.main import bp_main
from app.main.models import User, RideRequest, RideOffer, UserSchema,RideOfferSchema, RideRequestSchema

basic_auth = HTTPBasicAuth()


@bp_main.route('users',  methods=['POST'])
def create_user():
    data = request.get_json()
    user = User.get_user_by_email(data['email'])
    if user is None:
        user = User(data['email'],data['name'],data['phone'], data['password'])
        user.password = ""
        User.save(user)
        userSchema = UserSchema()
        usr = userSchema.dump(user)
        message = { 'user': usr,
                    'message': 'User Created Successfully'}
        response = jsonify(message)
        response.status_code = 201
        return response
    message = { 'user':'None',
                'message':'User Exists'}
    response = jsonify(message)
    response.status_code = 300
    return response


@bp_main.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    return jsonify({'token': token})


@basic_auth.verify_password
def verify_password(email, password):
    user = User.get_user_by_email(email)
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    pass
    message = {'message':'Unauthorized'}
    response = jsonify(message)
    response.status_code = 401
    return response


@bp_main.route('login', methods = ['POST'])
# @basic_auth.login_required
def login():
    data = request.get_json()
    user = User.get_user_by_email(data['email'])
    if user and basic_auth.verify_password(data['password']):
        g.current_user = user
        message = {'status':'Login Successfull',
                   'user':user.__repr__()}
        response = jsonify(message)
        response.status_code = 200
        return response
    else:
        message = {'status': 'Login Unsuccessfull'}
        response = jsonify(message)
        response.status_code = 403
        return response


@bp_main.route('users/<string:user_email>/rides', methods = ['POST'])
@basic_auth.login_required
def create_ride_offer(user_email, **kwargs):
    data = request.get_json()
    user = User.get_user_by_email(user_email)
    rideOffer = RideOffer(data['driver_email'], data['ride_date'], data['departure_time'], data['pick_up_point'], data['destination'], data['charges'])
    RideOffer.save(rideOffer)
    rideOfferSchema = RideOfferSchema()
    ride = rideOfferSchema.dump(rideOffer)
    msg = {'ride_offer': ride,
               'message':'Ride Offer Created Successfully'}
    response = jsonify(msg)
    response.status_code = 201
    return response


@bp_main.route('users/rides/<int:ride_id>', methods = ['GET'])
# @basic_auth.login_required
def get_a_ride_offer(ride_id, **kwargs):
    ride_offer = RideOffer.get_ride_by_id(ride_id)
    if ride_offer:
        rideOfferSchema = RideOfferSchema()
        ride = rideOfferSchema.dump(ride_offer)
        msg = {'ride_offer' : ride}
        response = jsonify(msg)
        response.status_code = 200
        return response
    message = {'ride_offer': 'None'}
    response = jsonify(message)
    response.status_code = 301
    return response


@bp_main.route('users/rides', methods = ['GET'])
# @basic_auth.login_required
def get_ride_offers():
    message = {}
    count = 1
    rideOffers = RideOffer.query.all()
    for ride in rideOffers:
        rideOfferSchema = RideOfferSchema()
        ride = rideOfferSchema.dump(ride)
        message[count] = ride
        count += 1
    response = jsonify(message)
    response.status_code = 200
    return response


@bp_main.route('users/rides/<int:ride_id>/requests', methods = ['POST'])
# @basic_auth.login_required
def request_ride(ride_id, **kwargs):
    data = request.get_json()
    rideRequest = RideRequest(ride_id, data['user_email'])
    RideRequest.save(rideRequest)
    rideRequestSchema = RideRequestSchema()
    ride_request = rideRequestSchema.dump(rideRequest)
    message = {'request': ride_request}
    response = jsonify(message)
    response.status_code = 201
    return response

@bp_main.route('users/rides/<int:ride_id>/requests', methods = ['GET'])
# @basic_auth.login_required
def get_all_requests_for_an_offer(ride_id, **kwargs):
    message = {}
    count = 1
    rideRequests = RideRequest.query.filter_by(ride_offer_id = ride_id)
    for ride_request in rideRequests:
        rideRequestSchema = RideRequestSchema()
        reqst = rideRequestSchema.dump(ride_request)
        message[count] = reqst
        count += 1
    response = jsonify(message)
    response.status_code = 200
    return response