from app import app, sec
import unittest
import json
from datetime import datetime
import re 
from users_details import MAX_CHARS, VALID_USER



class Club_Admin_Tests(unittest.TestCase):
    ''' Responsible for testing all administrator functionallity tests'''
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.sec = sec
        self.role = 'admin'

    def tearDown(self):
        pass

    # ============================ Booking & Cancellation Tests - Admin ============================
    def test_handle_booking_admin_sucessful(self):
        ''' ID: 44 '''
        with app.test_request_context('/api/handle_booking', method='PUT',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"court":"grass_one", "date":"2023-12-11", "time":"13", "user":"certified_user@outlook.com", "cancel":False}
            response = self.app.put('/api/handle_booking', data=json.dumps(load), content_type="application/json")
            response_object = json.loads(response.data.decode('utf-8'))
            self.assertTrue(response_object['title'] == "Booking Complete!")

    def test_handle_booking_admin_wrong_email(self):
        ''' ID: 45 '''
        with app.test_request_context('/api/handle_booking', method='PUT',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
            load = {"court":"grass_two", "date":"2023-11-19", "time":"17", "user":"NoUser", "cancel":False}
            response = self.app.put('/api/handle_booking', data=json.dumps(load), content_type="application/json")
            response_object = json.loads(response.data.decode('utf-8'))
            self.assertTrue(response_object['title'] == "Booking Error!")
    
    def test_handle_booking_admin_wrong_court(self):
        ''' ID: 46 '''
        with app.test_request_context('/api/handle_booking', method='PUT',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
            load = {"court":"grass_three", "date":"2023-11-19", "time":"17", "user":"certified_user@outlook.com", "cancel":False}
            response = self.app.put('/api/handle_booking', data=json.dumps(load), content_type="application/json")
            response_object = json.loads(response.data.decode('utf-8'))
            self.assertTrue(response_object['title'] == "Booking Error!")

    def test_handle_booking_admin_wrong_time(self):
        ''' ID: 47 '''
        with app.test_request_context('/api/handle_booking', method='PUT',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
            load = {"court":"grass_three", "date":"2023-11-19", "time":"2400", "user":"certified_user@outlook.com", "cancel":False}
            response = self.app.put('/api/handle_booking', data=json.dumps(load), content_type="application/json")
            response_object = json.loads(response.data.decode('utf-8'))
            self.assertTrue(response_object['title'] == "Booking Error!")

    def test_handle_cancellation_admin_sucessful(self):
        ''' ID: 48 '''
        with app.test_request_context('/api/handle_booking', method='PUT',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"court":"grass_one", "date":"2023-12-11", "time":"13", "user":"certified_user@outlook.com", "cancel":True}
            response = self.app.put('/api/handle_booking', data=json.dumps(load), content_type="application/json")
            response_object = json.loads(response.data.decode('utf-8'))
            self.assertTrue(response_object['title'] == "Booking Cancelled!")

    # ============================ Create User Tests - Admin ============================

    def test_create_club_member_admin_successful(self):
        ''' ID: 49 '''
        with app.test_request_context('/admin/create_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"firstname":"Josh", "lastname":"Doeer", "email":"createUser@outlook.com", "role":"user"}
            response = self.app.post('/admin/create_user', data=load)
            self.assertIn("Account Created Succesfully", response.data.decode('utf-8'))
    
    def test_create_admin_admin_successful(self):
        ''' ID: 50 '''
        with app.test_request_context('/admin/create_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"firstname":"Josh", "lastname":"Doeer", "email":"createAdmin@outlook.com", "role":"admin"}
            response = self.app.post('/admin/create_user', data=load)
            self.assertIn("Account Created Succesfully", response.data.decode('utf-8'))

    def test_create_user_admin_no_first_name(self):
        ''' ID: 51 '''
        with app.test_request_context('/admin/create_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"firstname":"", "lastname":"Doeer", "email":"admincreate1@outlook.com", "role":"user"}
            response = self.app.post('/admin/create_user', data=load)
            self.assertIn("Invalid First Name", response.data.decode('utf-8'))    
    
    def test_create_user_admin_max_first_name(self):
        ''' ID: 52 '''
        with app.test_request_context('/admin/create_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"firstname":MAX_CHARS, "lastname":"Doeer", "email":"admincreate2@outlook.com", "role":"user"}
            response = self.app.post('/admin/create_user', data=load)
            self.assertIn("Invalid First Name", response.data.decode('utf-8'))
    
    def test_create_user_admin_no_surname(self):
        ''' ID: 53 '''
        with app.test_request_context('/admin/create_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"firstname":"John", "lastname":"", "email":"admincreate3@outlook.com", "role":"user"}
            response = self.app.post('/admin/create_user', data=load)
            self.assertIn("Invalid Surname", response.data.decode('utf-8'))    
    
    def test_create_user_admin_max_surname(self):
        ''' ID: 54 '''
        with app.test_request_context('/admin/create_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"firstname":"John", "lastname":MAX_CHARS, "email":"admincreate4@outlook.com", "role":"user"}
            response = self.app.post('/admin/create_user', data=load)
            self.assertIn("Invalid Surname", response.data.decode('utf-8'))
    
    def test_create_user_admin_invalid_email(self):
        ''' ID: 55 '''
        with app.test_request_context('/admin/create_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"firstname":"John", "lastname":"Doeer", "email":"nouser.com", "role":"user"}
            response = self.app.post('/admin/create_user', data=load)
            self.assertIn("Invalid Email Address", response.data.decode('utf-8'))

    def test_create_user_admin_invalid_role(self):
        ''' ID: 56 '''
        with app.test_request_context('/admin/create_user', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
            load = {"firstname":"John", "lastname":"Doeer", "email":"admincreate5@outlook.com", "role":"invalid"}
            response = self.app.post('/admin/create_user', data=load)
            self.assertIn("Invalid Role", response.data.decode('utf-8'))  

    # ============================ Delete User Tests - Admin ============================

    def test_delete_user_admin_successful(self):
        ''' ID: 57 '''
        with app.test_request_context('/admin/delete_account', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
                sess['username'] = "certified_user@outlook.com"
            loads = [{"delete_pword":VALID_USER['password'], "email_delete":"createUser@outlook.com"},{"delete_pword":VALID_USER['password'], "email_delete":"createAdmin@outlook.com"}]
            for load in loads:
                response = self.app.post('/admin/delete_account', data=load)
                self.assertIn("Account Deleted!", response.data.decode('utf-8'))
    
    def test_delete_user_admin_failure(self):
        ''' ID: 58 '''
        with app.test_request_context('/admin/delete_account', method='POST',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = self.role
                sess['testing'] = True
                sess['username'] = "certified_user@outlook.com"
            loads = [{"delete_pword":VALID_USER['password'], "email_delete":"create.com"},{"delete_pword":VALID_USER['password'], "email_delete":"createAdmin.com"}]
            for load in loads:
                response = self.app.post('/admin/delete_account', data=load)
                self.assertIn("Error Deleting Account", response.data.decode('utf-8'))


