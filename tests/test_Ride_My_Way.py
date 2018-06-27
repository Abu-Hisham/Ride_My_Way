import unittest
import json
from app import create_app
from app.main.models import User, RideOffer, RideRequest


class RideMyWayTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.user1 = User('driver@gmail.com', 'Mohammed Rajab', '0700000000', 'aam123')
        self.user2 = User('abdulmoha786@gmail.com', 'Abdulaziz Rajab', '0701633016', 'aam786')
        self.rideOffer = RideOffer (1, self.user1.email, '7/7/2018', '1030', 'madaraka', 'makina', 250)
        self.rideRequest = RideRequest(1, 1,self.user2['email'])

    def test_user_generates_auth_token(self):
        pass

    def test_user_signup(self):
        res = self.client.post('api/v1/main/users/', data=json.dumps(self.user1.__repr__()), headers = {'content-type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        self.assertIn(res.data, 'driver@gmail.com')

    def test_user_login(self):
        pass

    def test_login_fails_for_incorrect_credentials(self):
        pass

    def test_duplicate_account_creation_fails(self):
        res = self.client.post('api/v1/main/users/', data=json.dumps(self.user1.__repr__()), headers = {'content-type': 'application/json'})
        self.assertEqual(res.status_code, 403)

    def test_user_can_create_ride_offer(self):
        res = self.client.post('api/v1/main/ride_offers/', data=json.dumps(self.rideOffer.__repr__()), headers = {'content-type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        self.assertIn(res.data, self.user1.email)

    def test_user_can_view_their_ride_offers(self):
        res = self.client.get('api/v1/main/ride_offers')
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.data, self.rideOffer.__repr__())

    def test_user_can_reschedule_ride_offer(self):
        new_time = {'time':'1530HRS'}
        res = self.client.put('api/v1/main/ride_offers/' + self.rideOffer.ride_id, data=json.dumps(new_time, headers = {'content-type': 'application/json'}))
        self.assertEqual(res.status_code, 200)
        # self.assertEqual(res.data, new_time)

    def test_user_can_request_ride_offer(self):
        res = self.client.post('api/v1/main/ride_offers/ride_requests/', data=json.dumps(self.rideRequest.__repr__(), headers = {'content-type': 'application/json'}))
        self.assertEqual(res.status_code, 201)
        self.assertDictEqual(res.data, self.rideRequest.__repr__())

    def test_user_can_view_ride_requests_for_an_offer(self):
        res = self.client.get('api/v1/main/ride_offers/' + self.rideOffer.ride_id + '/ride_requests')
        self.assertEqual(res.status_code, 200)
        self.assertIn(res.data, self.rideRequest.__repr__())

    def test_user_can_send_friend_request(self):
        pass

    def test_user_can_respond_to_friend_request(self):
        pass

    def test_user_can_cancel_ride_request(self):
        res = self.client.delete('api/v1/main/ride_offers/ride_requests' + self.rideRequest.request_id)
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.data, self.rideRequest.__repr__())

    def test_user_can_view_their_ride_requests(self):
        res = self.client.get('api/v1/main/ride_offers/ride_requests')
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.data, self.rideRequest.__repr__())
