class User(object):
    users = []

    def __init__(self, email, name, phone, password):
        self.email = email
        self.name = name
        self.phone = phone
        self.password_hash = self.generate_password_hash(password)
        self.friends = []
        self.messages = []

    def generate_password_hash(self, password):
        return password

    def create_ride_offer(self):
        pass

    def request_ride(self, ride_id):
        pass

    def send_friend_request(self, username):
        pass

    def accept_friend_request(self):
        pass

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

    def __repr__(self):
        return {
                'message_id': self.message_id,
                'recipient_email': self.recipient_email,
                'time': self.time,
                'message_title': self.messageTitle,
                'message_body': self.messageBody
               }