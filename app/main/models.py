class User(object):
    users = []

    def __init__(self):
        self.email = ""
        self.name = ""
        self.phone = ""
        self.pasword_hash = ""
        self.friends = []
        self.messages = []

    def create_ride_offer(self):
        pass

    def request_ride(self, ride_id):
        pass

    def send_friend_request(self, username):
        pass

    def accept_friend_request(self):
        pass


class RideOffer(object):
    ride_offers = []

    def __init__(self):
        self.ride_id = ""
        self.driver_email = ""
        self.ride_date = ""
        self.departure_time = ""
        self.pick_up_point = ""
        self.destination = ""
        self.charges = ""
        self.accepted_requests = []

    def cancel(self):
        pass

    def create(self):
        pass

    def reschedule(self):
        pass

    def respond_to_request(self, request_id):
        pass


class RideRequests(object):
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


class Message(object):
    messages = []

    def __init__(self):
        self.message_id = ""
        self.reciepient_email = ""
        self.time = ""
        self.messageTitle = ""
        self.messageBody = ""

    def delete(self):
        pass