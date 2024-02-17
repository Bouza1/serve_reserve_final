from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import binascii
import os
import dotenv
import string
import secrets
import re

class Sec:

    def __init__(self):
        dotenv.load_dotenv("var.env")
        self.key = os.environ['ENC_KEY']
        self.SECRET_KEY = binascii.unhexlify(self.key.encode('utf-8'))
        self.iv = os.environ['ENC_IV']
        self.FIXED_IV = binascii.unhexlify(self.iv.encode('utf-8'))
        self.backend = default_backend()
        self.cipher = Cipher(algorithms.AES(self.SECRET_KEY), modes.CBC(self.FIXED_IV), backend=self.backend)

    def enc(self, data):
        ''' Encrypts given date '''
        self.encryptor = self.cipher.encryptor()
        self.padded_data = data.encode() + b'\x00' * (16 - (len(data) % 16))
        self.encrypted_data = self.encryptor.update(self.padded_data) + self.encryptor.finalize()
        return base64.urlsafe_b64encode(self.encrypted_data).decode()

    def dec(self, enc_data):
        ''' Decrypts given data '''
        self.decryptor = self.cipher.decryptor()
        decrypted_data = self.decryptor.update(base64.urlsafe_b64decode(enc_data)) + self.decryptor.finalize()
        return decrypted_data.rstrip(b'\x00').decode()
    
    def generate_secure_password(self):
        ''' Generates a secure password which conforms too the requirements'''
        characters = string.ascii_letters + string.digits + string.punctuation
        password_length = max(8, secrets.randbelow(13))
        secure_password = ''
        secure_password += secrets.choice(string.ascii_uppercase)
        secure_password += secrets.choice(string.digits)
        secure_password += ''.join(secrets.choice(characters) for _ in range(password_length - 2))
        password_list = list(secure_password)
        secrets.SystemRandom().shuffle(password_list)
        secure_password = ''.join(password_list)
        return secure_password
    
    def is_email(self, email):
        ''' Checks if given parameter is that of an email address '''
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, email))

    def is_uk_postcode(postcode):
        postcode_pattern = re.compile(r'^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$')
        postcode = postcode.replace(" ", "").upper()
        return bool(postcode_pattern.match(postcode))

    def is_uk_phone_number(phone_number):
        phone_number_pattern = re.compile(r'^(?:(?:\+44)|(?:0))(?:(?:20\d{1}|11\d{1}|800\d{1})|(?:7[1-9]\d{1}|3[1-9]\d{1}|1[1-9]\d{1}|9[1-5]\d{1}))(?:\s?\d{4}\s?\d{3}|\d{10})$')
        phone_number = phone_number.replace(" ", "")
        return bool(phone_number_pattern.match(phone_number))
