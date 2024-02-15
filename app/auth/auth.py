from app.utils.db import DBHANDLER
from app import app, bcrypt

class Authenticate:

    def __init__(self):
        self.db = DBHANDLER()

    def get_user_security(self, username, password):
        ''' Handles Authentication against the database using email and password'''
        try:
            statement = "SELECT * FROM security WHERE id = %s"
            user = self.db.search_return_one(statement, username) 
            if bcrypt.check_password_hash(user[1], password):
                return {"token":True}
            else:
                return {"token":False, "error":"Incorrect Password!"}
        except:
            return {"token":False, "error":"No User Found"}

    def check_user_exists(self, username):
        ''' Returns wheter a user exists within the database'''
        try:
            statement = "SELECT * FROM security WHERE id = %s"
            user = self.db.search_return_one(statement, username)
            if user == None:
                return False
            else:
                return True
        except:
            return {"token":False, "error":"Error With The Server"}
