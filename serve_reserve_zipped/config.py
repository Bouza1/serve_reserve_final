import os
import dotenv

dotenv.load_dotenv("var.env")

DEBUG = True  
SECRET_KEY = os.environ['SECRET_KEY']
DB_URL = os.environ['DATABASE_URL']

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587 
MAIL_USE_TLS = True 
MAIL_USE_SSL = False 
MAIL_USERNAME = os.environ['EMAIL_USERNAME'] 
MAIL_PASSWORD = os.environ['EMAIL_PASSWORD'] 
MAIL_DEFAULT_SENDER = os.environ['EMAIL_USERNAME']


