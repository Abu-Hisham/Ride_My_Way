from werkzeug.security import generate_password_hash, check_password_hash
import base64
from datetime import datetime, timedelta
#from sqlalchemy.dialects.sqlite import DATETIME
import os
from app import db
from marshmallow import Schema, fields


class User(db.Model):

    __tablename__ = "users"

    email = db.Column(db.String(50), primary_key = True)
    name = db.Column(db.String(255))
    phone = db.Column(db.Integer)
    password_hash = db.Column(db.String(255))
    ride_offer_id = db.Column(db.Integer, db.ForeignKey('RideOffer.ride_id'))
    message_id = db.Column(db.Integer)
    token = db.Column(db.String(255))
    token_expiration = db.Column(db.Integer)

    def __init__(self, email, name, phone, password):
        self.email = email
        self.name = name
        self.phone = phone
        self.password = password
        self.password_hash = generate_password_hash(password)
        self.token = ""
        self.token_expiration = 0

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_token(self, expires_in = 3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token

    def generate_password_hash(self, password):
        self.password_hash = generate_password_hash (password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash (self.password_hash, password)

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_user_by_email(email):
        user = User.query.filter_by(email = email).first()
        return user

        # for user in User.users:
        #     if user.email == email:
        #         return user
        # return None

    def send_friend_request(self, username):
        pass

    def accept_friend_request(self):
        pass

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if self.__index >= len(User.users) - 1:
            raise StopIteration
        self.__index += 1
        user = User.user[self.__index]
        return user

    def __repr__(self):
        return {'email': self.email,
                'name': self.name,
                'phone': self.phone,
                'password': self.password
                }

class UserSchema(Schema):
    # class Meta:
    #     fields = ('email','name','phone','token')
    email = fields.Str()
    name = fields.Str()
    phone = fields.Str()
    token = fields.Str()


class RideOffer(db.Model):

    __tablename__ = "RideOffer"

    ride_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    driver_email = db.Column(db.String(50), db.ForeignKey('users.email'))
    ride_date = db.Column(db.String(15))
    departure_time = db.Column(db.String(8))
    pick_up_point = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    charges = db.Column(db.Integer)

    def __init__(self, driver_email, ride_date, departure_time,pick_up_point, destination, charges):
        self.driver_email = driver_email
        self.ride_date = ride_date
        self.departure_time = departure_time
        self.pick_up_point = pick_up_point
        self.destination = destination
        self.charges = charges

    def get_all_rides(self):
        rides = RideOffer.query.all()
        return rides

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_ride_by_id(id):
        ride = RideOffer.query.filter_by(ride_id = id).first()
        if ride:
            return ride
        else:
            return None
        # for ride in RideOffer.rideOffers:
        #     if ride.ride_id == ride_id:
        #         return ride
        # return None

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if self.__index >= len(RideOffer.ride_offers) - 1:
            raise StopIteration
        self.__index += 1
        rideOffer = RideOffer.ride_offers[self.__index]
        return rideOffer

    def __repr__(self):
        return {
                'ride_id':RideOffer.ride_id,
                'driver_email':self.driver_email,
                'ride_date':self.ride_date,
                'departure_time':self.departure_time,
                'pick_up_point': self.pick_up_point,
                'destination':self.destination,
                'charges':self.charges
               }


class RideOfferSchema(Schema):
    ride_id = fields.Int()
    driver_email = fields.Email()
    ride_date = fields.Str()
    departure_time = fields.Str()
    pick_up_point = fields.Str()
    destination = fields.Str()
    charges = fields.Int()


class RideRequest(db.Model):

    __tablename__ = "RideRequest"

    request_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    ride_offer_id = db.Column(db.Integer, db.ForeignKey('RideOffer.ride_id'))
    user_email = db.Column(db.String(50))
    status = db.Column(db.String(20))

    def __init__(self, ride_offer_id, user_email):
        self.ride_offer_id = ride_offer_id
        self.user_email = user_email
        self.status = "pending"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def cancel_request(self):
        pass

    def get_requests_for_an_offer(offer_id):
        request = RideRequest.query.filter_by(ride_offer_id= offer_id).first()
        if request:
            return request
        else:
            return None


class RideRequestSchema(Schema):
    request_id = fields.Int()
    ride_offer_id = fields.Int()
    user_email = fields.Email()

