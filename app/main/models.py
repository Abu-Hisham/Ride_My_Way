from werkzeug.security import generate_password_hash, check_password_hash
import base64
from datetime import datetime, timedelta
#from sqlalchemy.dialects.sqlite import DATETIME
import os
from app import db

from app.main import db


class User(object):

    def __init__(self, email, name, phone, password):
        self.email = email
        self.name = name
        self.phone = phone
        self.password_hash = generate_password_hash(password)
        self.token = ""
        self.token_expiration = 0

    def save(self):
        sql = """INSERT INTO users(email, name, phone, password_hash)
                 VALUES(%s,%s,%s,%s)"""
        cursor = db.postgres_connection.get_cursor()
        cursor.execute(sql, (self.email,self.name,self.phone,self.password_hash))
        db.postgres_connection.commit()

    def delete(self):
        pass

    def get_token(self, expires_in = 3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        sql = """UPDATE users SET token = %s, token_expiration = %s WHERE email = %s """
        cursor = db.postgres_connection.get_cursor()
        cursor.execute(sql, (self.token, self.token_expiration, self.email))
        db.postgres_connection.commit ()
        return self.token

    def generate_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_all():
        sql = """SELECT * FROM users"""
        cursor = db.postgres_connection.get_cursor ()
        cursor.execute(sql)
        db.postgres_connection.commit()
        results = cursor.fetchall()
        user_list = []
        for result in results:
            user = User(result[0], result[1], result[2], result[3])
            user.token = result[4]
            user.token_expiration = result[5]
            user_list.append(user)
        return user_list

    @staticmethod
    def get_user_by_email(email):
        sql = """SELECT * FROM users WHERE email = %s"""
        cursor = db.postgres_connection.get_cursor()
        cursor.execute(sql, (email,))
        user_data = cursor.fetchone()
        db.postgres_connection.commit()
        user = User(user_data[0], user_data[1], user_data[2], user_data[3])
        user.token = user_data[4]
        user.token_expiration = user_data[5]
        return user

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


class RideOffer(object):

    def __init__(self, driver_email, ride_date, departure_time, pick_up_point, destination, charges):
        self.ride_id = 0
        self.driver_email = driver_email
        self.ride_date = ride_date
        self.departure_time = departure_time
        self.pick_up_point = pick_up_point
        self.destination = destination
        self.charges = charges


    @staticmethod
    def get_all_rides():
        sql = """SELECT * FROM \"RideOffer\" """
        cursor = db.postgres_connection.get_cursor ()
        cursor.execute (sql)
        db.postgres_connection.commit ()
        results = cursor.fetchall ()
        ride_list = []
        for result in results:
            ride = RideOffer(result[1], result[2], result[3], result[4], result[5], result[6])
            ride.ride_id = result[0]
            ride_list.append(ride)
        return ride_list

    def save(self):
        sql = """INSERT INTO \"RideOffer\"(driver_email, ride_date, departure_time, pick_up_point, destination, charges)
                         VALUES(%s,%s,%s,%s,%s,%s)"""
        cursor = db.postgres_connection.get_cursor()
        cursor.execute(sql, (self.driver_email, self.ride_date, self.departure_time, self.pick_up_point, self.destination, self.charges))
        db.postgres_connection.commit()

    def delete(self):
        pass

    @staticmethod
    def get_ride_by_id(ride_id):
        sql = """SELECT * FROM \"RideOffer\" WHERE ride_id = %s """
        cursor = db.postgres_connection.get_cursor()
        cursor.execute(sql, (ride_id,))
        ride_data = cursor.fetchone()
        db.postgres_connection.commit()
        if ride_data:
            ride = RideOffer(ride_data[1], ride_data[2], ride_data[3], ride_data[4], ride_data[5], ride_data[6])
            ride.ride_id = ride_data[0]
            return ride.__repr__()
        else:
            return None

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
                'departure_time':self.departure_time,
                'pick_up_point': self.pick_up_point,
                'destination':self.destination,
                'charges':self.charges
               }


class RideRequest(object):
    def __init__(self, ride_offer_id, user_email):
        self.request_id = 0
        self.ride_offer_id = ride_offer_id
        self.user_email = user_email
        self.status = "pending"

    def save(self):
        sql = """INSERT INTO \"RideRequest\"(ride_offer_id, user_email, status)
                         VALUES(%s,%s,%s)"""
        cursor = db.postgres_connection.get_cursor ()
        cursor.execute(sql, (self.ride_offer_id, self.user_email, self.status))
        db.postgres_connection.commit()

    def get_request_id(self):
        pass

    @staticmethod
    def delete(request_id):
        sql = """DELETE FROM \"RideRequest\" where request_id = %d"""
        cursor = db.postgres_connection.get_cursor()
        cursor.execute (sql, (request_id,))
        db.postgres_connection.commit()

    @staticmethod
    def get_requests_for_an_offer(offer_id):
        sql = """SELECT * FROM \"RideRequest\" WHERE ride_offer_id = %s"""
        cursor = db.postgres_connection.get_cursor()
        cursor.execute(sql, (offer_id,))
        request_data = cursor.fetchall()
        db.postgres_connection.commit()
        requests_list = []
        for request in request_data:
            ride_request = RideRequest(request[1], request[2])
            ride_request.request_id = request[0]
            requests_list.append(ride_request)
        return requests_list

    def __repr__(self):
        return {
                'request_id':self.request_id,
                'ride_offer_id':self.ride_offer_id,
                'user_email':self.user_email,
                'status':self.status
                }
