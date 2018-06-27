from werkzeug.security import generate_password_hash, check_password_hash
import base64
from datetime import datetime, timedelta
import os

class User(object):
    users = []

    def __init__(self, email, name, phone, password):
        self.email = email
        self.name = name
        self.phone = phone
        self.password_hash = self.generate_password_hash(password)
        self.friends = []
        self.messages = []
        self.token = ""
        self.token_expiration = 0

    def get_token(self, expires_in = 3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        return self.token

    def generate_password_hash(self, password):
        self.password_hash = generate_password_hash (password)

    def check_password(self, password):
        return check_password_hash (self.password_hash, password)

    def create_ride_offer(self):
        pass

    def request_ride(self, ride_id):
        pass

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
        return {'email':self.email,
                'name': self.name,
                'phone':self.phone,
                }


class RideOffer(object):
    ride_offers = []

    def __init__(self, ride_id, driver_email, ride_date, departure_time,pick_up_point, destination, charges):
        self.ride_id = ride_id
        self.driver_email = driver_email
        self.ride_date = ride_date
        self.departure_time = departure_time
        self.pick_up_point = pick_up_point
        self.destination = destination
        self.charges = charges
        self.accepted_requests = []

    def cancel(self):
        pass

    def create(self):
        pass

    def reschedule(self):
        pass

    def respond_to_request(self, request_id):
        pass

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
                'ride_id':self.ride_id,
                'driver_email':self.driver_email,
                'ride_date':self.ride_date,
                'departdure_time':self.departure_time,
                'pick_up_point': self.pick_up_point,
                'destination':self.destination,
                'charges':self.charges
               }


class RideRequest(object):
    ride_requests = []

    def __init__(self):
        self.request_id = ""
        self.ride_offer_id = ""
        self.user_email = ""
        self.status = ()

    def cancel_request(self):
        pass

    def notify_user(self, userEmail):
        pass

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if self.__index >= len(RideRequest.ride_requests) - 1:
            raise StopIteration
        self.__index += 1
        rideRequest = RideRequest.ride_requests[self.__index]
        return rideRequest

    def __repr__(self):
        return {
                'request_id': self.request_id,
                'ride_offer_id': self.ride_offer_id,
                'user_email': self.user_email
               }


class Message(object):
    messages = []

    def __init__(self):
        self.message_id = ""
        self.recipient_email = ""
        self.time = ""
        self.messageTitle = ""
        self.messageBody = ""

    def delete(self):
        pass

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if self.__index >= len(Message.messages) - 1:
            raise StopIteration
        self.__index += 1
        message = Message.messages[self.__index]
        return message

    def __repr__(self):
        return {
                'message_id': self.message_id,
                'recipient_email': self.recipient_email,
                'time': self.time,
                'message_title': self.messageTitle,
                'message_body': self.messageBody
               }