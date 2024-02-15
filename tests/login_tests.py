from app import app, sec
import unittest
from users_details import EMAIL_DOESNT_EXIST, VALID_CLUB_MEMBER, VALID_ADMIN, WRONG_PASSWORD

class Login_Tests(unittest.TestCase):
    ''' Responsible for testing all login functionallity '''
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.sec = sec

    def tearDown(self):
        pass
    # =========================================== Login Tests ====================================
    def test_login_club_member(self):
        ''' ID: 7 '''
        response = self.app.post('/login', data=VALID_CLUB_MEMBER, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<title>User Dashboard</title>', response.data.decode('utf-8'))

    def test_login_admin(self):
        ''' ID: 8 '''
        response = self.app.post('/login', data=VALID_ADMIN, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<title>Admin Dashboard</title>', response.data.decode('utf-8'))

    def test_login_incorrect_email(self):
        ''' ID: 9 '''
        response = self.app.post('/login', data=EMAIL_DOESNT_EXIST, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('No User Found', response.data.decode('utf-8'))

    def test_login_wrong_password(self):
        ''' ID: 10 '''
        response = self.app.post('/login', data=WRONG_PASSWORD, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Incorrect Password!', response.data.decode('utf-8'))
