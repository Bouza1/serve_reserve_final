from app import app, sec
import unittest
import json
from users_details import MAX_CHARS, SAFE_CREATE_DELETE, USER_DOESNT_EXISTS, USER_EXISTS, VALID_USER

class Club_Member_Tests(unittest.TestCase):
    ''' Responsible for testing all club member functionallity tests '''
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.sec = sec
        self.role = 'user'

    def tearDown(self):
        pass
    # ============================ Booking & Cancellation Tests ============================
    def test_handle_booking_club_member_sucessful(self):
        ''' ID: 29 '''
        with app.test_request_context('/api/handle_booking', method='PUT',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
            load = {"court":"grass_one", "date":"2023-12-11", "time":"13", "user":self.sec.enc("certified_user@outlook.com"), "cancel":False}
            response = self.app.put('/api/handle_booking', data=json.dumps(load), content_type="application/json")
            response_object = json.loads(response.data.decode('utf-8'))
            self.assertTrue(response_object['title'] == "Booking Complete!")
            
    def test_handle_booking_user_wrong_email(self):
        ''' ID: 30 '''
        with app.test_request_context('/api/handle_booking', method='PUT',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
            load = {"court":"grass_two", "date":"2023-11-19", "time":"17", "user":self.sec.enc("NoUser"), "cancel":False}
            response = self.app.put('/api/handle_booking', data=json.dumps(load), content_type="application/json")
            response_object = json.loads(response.data.decode('utf-8'))
            self.assertTrue(response_object['title'] == "Booking Error!")
    
    def test_handle_booking_user_wrong_court(self):
        ''' ID: 31'''
        with app.test_request_context('/api/handle_booking', method='PUT',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
            load = {"court":"grass_three", "date":"2023-11-19", "time":"17", "user":self.sec.enc("certified_user@outlook.com"), "cancel":False}
            response = self.app.put('/api/handle_booking', data=json.dumps(load), content_type="application/json")
            response_object = json.loads(response.data.decode('utf-8'))
            self.assertTrue(response_object['title'] == "Booking Error!")

    def test_handle_booking_user_wrong_time(self):
        ''' ID: 32 '''
        with app.test_request_context('/api/handle_booking', method='PUT',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
            load = {"court":"grass_three", "date":"2023-11-19", "time":"2400", "user":self.sec.enc("certified_user@outlook.com"), "cancel":False}
            response = self.app.put('/api/handle_booking', data=json.dumps(load), content_type="application/json")
            response_object = json.loads(response.data.decode('utf-8'))
            self.assertTrue(response_object['title'] == "Booking Error!")

    def test_handle_cancellation_user_sucessful(self):
        ''' ID: 33 '''
        with app.test_request_context('/api/handle_booking', method='PUT',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
            load = {"court":"grass_one", "date":"2023-12-11", "time":"13", "user":self.sec.enc("certified_user@outlook.com"), "cancel":True}
            response = self.app.put('/api/handle_booking', data=json.dumps(load), content_type="application/json")
            response_object = json.loads(response.data.decode('utf-8'))
            self.assertTrue(response_object['title'] == "Booking Cancelled!")

    # ============================ Club Member Registration Tests ============================
    # ======================= START AI =======================
    def test_register_new_club_member_success(self):
        ''' ID: 34 - If test fails please run test 41 first '''
        # Send a POST request to the route
        response = self.app.post('/register_user', data=SAFE_CREATE_DELETE)
        # Check if the response is as expected
        self.assertEqual(response.status_code, 200)  # Replace with the actual status code returned on success
        # Add more assertions based on the expected behavior of your route
        self.assertIn('Account Created!', response.data.decode('utf-8'))
    # ======================= END AI =======================

    def test_register_new_club_member_user_exists(self):
        ''' ID: 35 '''
        response = self.app.post('/register_user', data=USER_EXISTS)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Username Already Exists', response.data.decode('utf-8'))


    def test_register_new_club_member_no_first_name(self):
        ''' ID: 36 '''
        with app.test_request_context('/register_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"fname":"", "lname":"Doeer", "email":"admincreate1@outlook.com", "role":"user"}
            response = self.app.post('/register_user', data=load)
            self.assertIn("Invalid First Name", response.data.decode('utf-8'))    
    
    def test_register_new_club_member_max_first_name(self):
        ''' ID: 37 '''
        with app.test_request_context('/register_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"fname":MAX_CHARS, "lname":"Doeer", "email":"admincreate2@outlook.com", "role":"user"}
            response = self.app.post('/register_user', data=load)
            self.assertIn("Invalid First Name", response.data.decode('utf-8'))
    
    def test_register_new_club_member_no_surname(self):
        ''' ID: 38 '''
        with app.test_request_context('/register_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"fname":"John", "lname":"", "email":"admincreate3@outlook.com", "role":"user"}
            response = self.app.post('/register_user', data=load)
            self.assertIn("Invalid Surname", response.data.decode('utf-8'))    
    
    def test_register_new_club_member_max_surname(self):
        ''' ID: 39 '''
        with app.test_request_context('/register_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"fname":"John", "lname":MAX_CHARS, "email":"admincreate4@outlook.com", "role":"user"}
            response = self.app.post('/register_user', data=load)
            self.assertIn("Invalid Surname", response.data.decode('utf-8'))
    
    def test_register_new_club_member_invalid_email(self):
        ''' ID: 40 '''
        with app.test_request_context('/register_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"fname":"John", "lname":"Doeer", "email":"nouser.com", "role":"user"}
            response = self.app.post('/register_user', data=load)
            self.assertIn("Invalid Email Address", response.data.decode('utf-8'))

    def test_register_new_club_member_invalid_role(self):
        ''' ID: 41 '''
        with app.test_request_context('/register_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"fname":"John", "lname":"Doeer", "email":"admincreate5@outlook.com", "role":"invalid"}
            response = self.app.post('/register_user', data=load)
            self.assertIn("Invalid Role", response.data.decode('utf-8'))  


    # ============================ Club Member Delete Account Functionallity Tests ============================
    def test_delete_own_account_success(self):
        ''' ID: 41 - If test fails please run test 34 First'''
        with app.test_request_context('/user/delete_account', method='POST', content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['username'] = SAFE_CREATE_DELETE['email']
            load = {'delete_pword': SAFE_CREATE_DELETE['password']}
            response = self.app.post('/user/delete_account', data=load)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Your Account Has Been Succesfully Deleted', response.data.decode('utf-8'))

    def test_delete_own_account_failure(self):
        ''' ID: 42 '''
        with app.test_request_context('/user/delete_account', method='POST', content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['username'] = USER_DOESNT_EXISTS['email']
                sess['testing'] = True
            load = {'delete_pword': USER_DOESNT_EXISTS['password']}
            response = self.app.post('/user/delete_account', data=load)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Error Deleting Account, Incorrect Email!', response.data.decode('utf-8'))



