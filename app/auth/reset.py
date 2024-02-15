from app import app, bcrypt
import os
import base64
from app.utils.db import DBHANDLER
from app.utils.security import Sec


class Reset_Token:
        
    def __init__(self, email):
        self.email = email
        self.sec = Sec()
        self.token = self.create_token()

    def generate_url_safe_variable(self):
        ''' Generates a Safe URL Variable '''
        random_bytes = os.urandom(32) # AI
        url_safe_variable = base64.urlsafe_b64encode(random_bytes).rstrip(b'=').decode() # AI
        return url_safe_variable # AI

    def create_token(self):
        ''' Creates an returns an encrypted and decrypted version of a token '''
        url = self.generate_url_safe_variable()
        encrypted = self.sec.enc(url)
        obj_e = {
            "id":encrypted,
            "token":0,
            "assigned":self.sec.enc(self.email)
        }
        obj_d = {
            "id":url,
            "token":0,
            "assigned":self.email
        }
        return {"E":obj_e, "D":obj_d}

    def spend_previous_tokens(self, assigned):
        ''' Invalidates all previous tokens within the database '''
        db = DBHANDLER()
        tokens = db.search_return_all("SELECT id FROM resets WHERE assigned = %s AND token = '0'", (assigned,))
        for token in tokens:
            self.spend_token(token)

    def insert_token(self):
        ''' Inserts a new token to the database '''
        db = DBHANDLER()
        db.insert_into("INSERT INTO resets (id, token, assigned) VALUES (%s, %s, %s)", (self.token['E']['id'], self.token['E']['token'], self.token['E']['assigned']))

    def spend_token(self, token_id):
        ''' Invalidates a given token within the database '''
        db = DBHANDLER()
        db.insert_into("UPDATE resets SET token = '1' WHERE id = %s", (token_id,))
    
