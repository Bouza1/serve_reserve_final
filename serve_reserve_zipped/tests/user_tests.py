from app import app, sec
import unittest
import json
from users_details import EMAIL_DOESNT_EXIST, MAX_CHARS, SAFE_CREATE_DELETE, USER_DOESNT_EXISTS, USER_EXISTS, VALID_USER

class User_Tests(unittest.TestCase):
    ''' Responsible for testing all user functionallity, those functionns shared by both club members and administrators '''
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.sec = sec
        self.roles = ['user', 'admin']

    def tearDown(self):
        pass

    # ============================================ Change Password Tests ============================================
    def test_change_password_success(self):
        ''' ID: 10 '''
        for role in self.roles:
            with app.test_request_context('/user/change_password', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                loads = [{'new_pword': SAFE_CREATE_DELETE['password']}, {'new_pword':VALID_USER['password']}]
                for load in loads:
                    response = self.app.post('/user/change_password', data=load)
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('Password Changed Successfully!', response.data.decode('utf-8'))

    def test_change_password_failure(self):
        ''' ID: 11 '''
        for role in self.roles:
            with app.test_request_context('/user/change_password', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = EMAIL_DOESNT_EXIST['username']
                    sess['testing'] = True
                load = {'new_pword': SAFE_CREATE_DELETE['password']}
                response = self.app.post('/user/change_password', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Error! The Request To Change Your Password Has Failed!', response.data.decode('utf-8'))

    # ============================================ User Profile Tests ============================================
    def test_update_profile_success(self):
        ''' ID: 12 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':"Test", "lastname":"Tester", "housenum":"87", "street":"Test Street", "town":"Test Town", "postcode":"TE579ME", "phonenum":"077456077456", "hidden_email":"certified_account@outlook.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Profile Updated Successfully!', response.data.decode('utf-8'))

    def test_update_profile_failure_no_first_name(self):
        ''' ID: 13 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':"", "lastname":"Tester", "housenum":"87", "street":"Test Street", "town":"Test Town", "postcode":"TE579ME", "phonenum":"077456077456", "hidden_email":"certified_account@outlook.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Invalid First Name, Please enter a first name between 3 - 150 characters in length', response.data.decode('utf-8'))

    def test_update_profile_failure_first_name_to_long(self):
        ''' ID: 14 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':MAX_CHARS, "lastname":"Tester", "housenum":"87", "street":"Test Street", "town":"Test Town", "postcode":"TE579ME", "phonenum":"077456077456", "hidden_email":"certified_account@outlook.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Invalid First Name, Please enter a first name between 3 - 150 characters in length', response.data.decode('utf-8'))

    def test_update_profile_failure_no_last_name(self):
        ''' ID: 15 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':"Test", "lastname":"", "housenum":"87", "street":"Test Street", "town":"Test Town", "postcode":"TE579ME", "phonenum":"077456077456", "hidden_email":"certified_account@outlook.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Invalid Surname, Please enter surname between 3 - 150 characters in length', response.data.decode('utf-8'))
    
    def test_update_profile_failure_last_name_too_long(self):
        ''' ID: 16 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':"Test", "lastname":MAX_CHARS, "housenum":"87", "street":"Test Street", "town":"Test Town", "postcode":"TE579ME", "phonenum":"077456077456", "hidden_email":"certified_account@outlook.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Invalid Surname, Please enter surname between 3 - 150 characters in length', response.data.decode('utf-8'))

    def test_update_profile_failure_invalid_house_num(self):
        ''' ID: 17 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':"Test", "lastname":"Tester", "housenum":MAX_CHARS, "street":"Test Street", "town":"Test Town", "postcode":"TE579ME", "phonenum":"077456077456", "hidden_email":"certified_account@outlook.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Invalid House Number, Please enter House Number no more than 150 characters in length', response.data.decode('utf-8'))

    def test_update_profile_failure_street_too_long(self):
        ''' ID: 18 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':"Test", "lastname":"Tester", "housenum":"87", "street":MAX_CHARS, "town":"Test Town", "postcode":"TE579ME", "phonenum":"077456077456", "hidden_email":"certified_account@outlook.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Invalid Street Address, Please enter Street Address no more than 150 characters in length', response.data.decode('utf-8'))

    def test_update_profile_failure_street_too_short(self):
        ''' ID: 19 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':"Test", "lastname":"Tester", "housenum":"87", "street":"AAA", "town":"Test Town", "postcode":"TE579ME", "phonenum":"077456077456", "hidden_email":"certified_account@outlook.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Invalid Street Address, Please enter Street Address no more than 150 characters in length', response.data.decode('utf-8'))

    def test_update_profile_failure_town_too_long(self):
        ''' ID: 20 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':"Test", "lastname":"Tester", "housenum":"87", "street":"Test Street", "town":MAX_CHARS, "postcode":"TE579ME", "phonenum":"077456077456", "hidden_email":"certified_account@outlook.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Invalid Town Address, Please enter a town no more than 90 characters in length', response.data.decode('utf-8'))

    def test_update_profile_failure_town_too_short(self):
        ''' ID: 21 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':"Test", "lastname":"Tester", "housenum":"87", "street":"Test Street", "town":"AAA", "postcode":"TE579ME", "phonenum":"077456077456", "hidden_email":"certified_account@outlook.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Invalid Town Address, Please enter a town no more than 90 characters in length', response.data.decode('utf-8'))

    def test_update_profile_failure_postcode_wrong(self):
        ''' ID: 22 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':"Test", "lastname":"Tester", "housenum":"87", "street":"Test Street", "town":"Test Town", "postcode":"sss", "phonenum":"077456077456", "hidden_email":"certified_account@outlook.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Invalid PostCode, Please enter a valid postcode. For Example DT117HD or DT11 7HD', response.data.decode('utf-8'))    

    def test_update_profile_failure_phonenum(self):
        ''' ID: 23 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':"Test", "lastname":"Tester", "housenum":"87", "street":"Test Street", "town":"Test Town", "postcode":"TE579ME", "phonenum":"abcde", "hidden_email":"certified_account@outlook.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn("Invalid Phone Number, Please enter a valid UK Phone Number", response.data.decode('utf-8'))    

    def test_update_profile_failure_email(self):
        ''' ID: 24 '''
        for role in self.roles:
            with app.test_request_context('/user/update_profile', method='POST', content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = role
                    sess['username'] = VALID_USER['username']
                    sess['testing'] = True
                load = {'firstname':"Test", "lastname":"Tester", "housenum":"87", "street":"Test Street", "town":"Test Town", "postcode":"TE579ME", "phonenum":"077456077456", "hidden_email":"noemail.com"}
                response = self.app.post('/user/update_profile', data=load)
                self.assertEqual(response.status_code, 200)
                self.assertIn("Invalid Email Address, Please Contact The Club Directly", response.data.decode('utf-8'))

