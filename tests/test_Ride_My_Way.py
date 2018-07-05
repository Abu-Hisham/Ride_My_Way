import unittest
import json
from app import create_app, db
from app.main.models import User, RideOffer, RideRequest, UserSchema, RideOfferSchema


#from base64 import b64encode


class RideMyWayTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.user1 = User('driver@gmail.com', 'Mohammed Rajab', '0700000000', 'aam123')
        self.user2 = User('abdulmoha786@gmail.com', 'Abdulaziz Rajab', '0701633016', 'aam786')
        self.rideOffer = RideOffer ( self.user1.email, '07/07/2018', '1030HRS', 'madaraka', 'makina', 250)
        self.rideRequest = RideRequest( 1,self.user2.email)
        with self.app.app_context():
            db.create_all()

    def test_user_generates_auth_token(self):
        pass

    def test_can_user_signup(self):
        # res = self.client.post('app/v1/main/users', data=json.dumps(self.user1.__repr__()), headers = {'content-type': 'application/json'})
        # self.assertEqual(res.status_code, 201)
        pass

    def test_user_login(self):
        pass

    def test_login_fails_for_incorrect_credentials(self):
        pass

    def test_duplicate_account_creation_fails(self):
        #res1 = self.client.post('app/v1/main/users', data=json.dumps(self.user1.__repr__()), headers = {'content-type': 'application/json'})
        res2 = self.client.post('app/v1/main/users', data=json.dumps(self.user1.__repr__()), headers = {'content-type': 'application/json'})
        self.assertNotEqual(res2.status_code, 201)

    def test_user_can_create_ride_offer(self):
        # token = self.user1.get_token()
        # res = self.client.post('app/v1/main/users/'+ self.user1.email + '/rides', data=json.dumps(self.rideOffer__repr__()),
        #                        headers = {'content-type': 'application/json',
        #                                   'Authorization': 'Basic ' + token})
        # self.assertEqual(res.status_code, 201)
        pass

    def test_user_can_fetch_a_ride_offer(self):
        # self.client.post('app/v1/main/users', data=json.dumps (self.user2.__repr__ ()),
        #                   headers={'content-type': 'application/json'})
        # res = self.client.get('app/v1/main/users/rides/1')
        # self.assertEqual(res.status_code, 200)
        pass

    def test_user_can_reschedule_ride_offer(self):
        pass
        # new_time = {'time':'1530HRS'}
        # res = self.client.put('app/v1/main/ride_offers/' + str(self.rideOffer.ride_id), data=json.dumps(new_time), headers = {'content-type': 'application/json'})
        # self.assertEqual(res.status_code, 200)
        # # self.assertEqual(res.data, new_time)

    def test_user_can_request_ride_offer(self):
        # self.client.post('app/v1/main/users', data=json.dumps (self.user1.__repr__ ()),
        #                   headers={'content-type': 'application/json'})
        # token =""
        # self.client.post('app/v1/main/users/'+ self.user1.email + '/rides', data=json.dumps(self.rideOffer.__repr__()),
        #                        headers = {'content-type': 'application/json',
        #                                   'Authorization': 'Basic ' + token})
        # res = self.client.post('app/v1/main/users/rides/1/requests', data=json.dumps(self.rideRequest.__repr__()), headers = {'content-type': 'application/json'})
        # self.assertEqual(res.status_code, 201)
        pass

    def test_user_can_view_ride_requests_for_an_offer(self):
        pass

    def test_user_can_send_friend_request(self):
        pass

    def test_user_can_respond_to_friend_request(self):
        pass

    def test_user_can_cancel_ride_request(self):
        pass
        # res = self.client.delete('app/v1/main/ride_offers/ride_requests' + str(self.rideRequest.request_id))
        # self.assertEqual(res.status_code, 200)
        # self.assertDictEqual(res.data, self.rideRequest.__repr__())

    # def test_user_can_view_their_ride_requests(self):
    #     res = self.client.get('app/v1/main/ride_offers/ride_requests')
    #     self.assertEqual(res.status_code, 200)
    #     self.assertDictEqual(res.data, self.rideRequest.__repr__())

    def tearDown(self):
            """teardown all initialized variables."""
            with self.app.app_context():
                # drop all tables
                db.session.remove()
                db.drop_all()