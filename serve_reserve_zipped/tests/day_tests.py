from app import app, sec
import unittest
import json
from datetime import datetime
import re 


class Court_Schedule_Tests(unittest.TestCase):
    ''' Responsible for testing all court schedule functionallity '''
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.sec = sec
        self.date_courts = [{'date': '2023-11-18', 'court': 'grass_one'},{'date': '2023-11-14', 'court': 'grass_two'},{'date': '2023-11-20', 'court': 'clay_one'}]

    def tearDown(self):
        pass

    def test_times_booked_user_success(self):
        ''' ID: 25 '''
        for court_time_object in self.date_courts:
            with app.test_request_context('/api/times_booked', method='PUT',content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = 'user'
                load = {'date': court_time_object['date'], 'court': court_time_object['court']}
                response = self.app.put('/api/times_booked', data=json.dumps(load),  content_type='application/json')
                repsonse_object = json.loads(response.data.decode('utf-8'))
                self.assertIn('times', repsonse_object)
                times = repsonse_object['times']   
                self.assertEqual(15, len(times))
                self.assertTrue(self.is_date(times[1]))
                for i in range(2, len(times)):
                    if times[i] == '0':
                        self.assertTrue(self.is_0_or_email(times[i]))
                    else:
                        decrypted = self.sec.dec(times[i])
                        self.assertTrue(self.is_0_or_email(decrypted))
        
    def test_times_booked_admin(self):
        ''' ID: 26 '''
        for court_time_object in self.date_courts:
            with app.test_request_context('/api/times_booked', method='PUT',content_type='application/json'):
                with self.app.session_transaction() as sess:
                    sess['role'] = 'admin'
                load = {'date': court_time_object['date'], 'court': court_time_object['court']}
                response = self.app.put('/api/times_booked', data=json.dumps(load),  content_type='application/json')
                repsonse_object = json.loads(response.data.decode('utf-8'))
                self.assertIn('times', repsonse_object)
                times = repsonse_object['times']   
                self.assertEqual(15, len(times))
                self.assertTrue(self.is_date(times[1]))
                for i in range(2, len(times)):
                    self.assertTrue(self.is_0_or_email(times[i]))
    
    def test_times_booked_user_wrong_date(self):
        ''' ID: 27 '''
        with app.test_request_context('/api/times_booked', method='PUT',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = 'user'
            load = {'date': 'aaaaaaaaaaa', 'court': 'grass_two'}
            response = self.app.put('/api/times_booked', data=json.dumps(load),  content_type='application/json')
            repsonse_object = json.loads(response.data.decode('utf-8'))
            self.assertIn("error", repsonse_object['times'])
    
    def test_times_booked_wrong_court(self):
        ''' ID: 28 '''
        with app.test_request_context('/api/times_booked', method='PUT',content_type='application/json'):
            with self.app.session_transaction() as sess:
                sess['role'] = 'user'
            load = {'date': '2023-11-18', 'court': 'wrong_court'}
            response = self.app.put('/api/times_booked', data=json.dumps(load),  content_type='application/json')
            repsonse_object = json.loads(response.data.decode('utf-8'))
            self.assertIn("error", repsonse_object['times'])
            self.assertIn("Failed to get times", repsonse_object['times']['error'])
            

    def is_date(self, date):
        try:
            date_object = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
            return True
        except Exception as e:
            return False

    def is_0_or_email(self, booking):
            is_0 = booking == '0'
            is_email = re.match(r"[^@]+@[^@]+\.[^@]+", booking) is not None # AI
            return is_0 or is_email
            

    def test_is_date(self):
        good_dates = ['Fri, 17 Nov 2023 00:00:00 GMT', 'Sun, 12 Nov 2023 00:00:00 GMT']
        bad_dates = ['A', '12/11/2023', 0, None, 'ABC', 'Tuesday']
        for date in good_dates:
            self.assertTrue(self.is_date(date))
        for date in bad_dates:
            self.assertFalse(self.is_date(date))

    def test_is_0_or_email(self):
        good_arr = ['0', 'adminadmin@outlook.co.uk', 'certified_user@outlook.com', 'emailemail@email.net', '0']
        bad_arr = ['7', 'abcdef', 'certified_user@gmail', 'one']
        for test in good_arr:
            self.assertTrue(self.is_0_or_email(str(test)))
        for test in bad_arr:
            self.assertFalse(self.is_0_or_email(test))
    