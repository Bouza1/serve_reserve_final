from app import app, sec
import unittest

class Page_Tests(unittest.TestCase):
    ''' Responsible for testing all pages accesibillity '''
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.sec = sec

    def tearDown(self):
        pass

    def test_login_page(self):
        ''' ID: 1 '''
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<title>Login</title>', response.data.decode('utf-8'))

    def test_register_page(self):
        ''' ID: 2 '''
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<title>Register</title>', response.data.decode('utf-8'))

    def test_user_dashboard_no_login(self):
        ''' ID: 3 '''
        response = self.app.get('/user/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Access Denied', response.data.decode('utf-8'))

    def test_admin_dashboard_no_login(self):
        ''' ID: 4 '''
        response = self.app.get('/admin/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Access Denied', response.data.decode('utf-8'))
    
    def test_reset_page_no_token(self):
        ''' ID: 5 '''
        response = self.app.get('/reset_link/aaaa')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid Reset Token!', response.data.decode('utf-8'))
        