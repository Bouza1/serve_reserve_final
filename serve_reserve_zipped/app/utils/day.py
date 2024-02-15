from app.utils.db import DBHANDLER
from app.utils.security import Sec
from flask import session

class Day:
    def __init__(self, date, court):
        self.day = date
        self.court = court
        self.sec = Sec()

    def get_times_for_day(self):
        ''' Returns the times a predefienced court is booked on a predefined date '''
        db = DBHANDLER()
        try:
            return db.search_return_one("SELECT * FROM {} WHERE day = %s".format(self.court), (self.day))
        except Exception as e:
            print(e)
            return{'error':"Failed to get times, please try refresh your broswer! If the problem persists please contact the club directly who can assist with court availability"}

    def insert_new_date(self):
        ''' Inserts a new date into the database '''
        db = DBHANDLER()
        return db.insert_into("INSERT INTO {} (day, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen) VALUES (%s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)".format(self.court), (self.day,))

    def check_for_day(self):
        ''' Checks if date exists in database and acts accordingly '''
        results = self.get_times_for_day()
        if not results:
            self.insert_new_date()
            return self.get_times_for_day()
        else:
            return results
