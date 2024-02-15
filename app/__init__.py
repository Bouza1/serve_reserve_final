from app.utils.security import Sec
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')
bcrypt = Bcrypt(app)
mail = Mail(app)
sec = Sec()

from app.auth.auth_routes import auth_routes
from app.user.user_routes import user_routes
from app.admin.admin_routes import admin_routes
from app.api.api_routes import api_routes

app.register_blueprint(auth_routes, url_prefix='/')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(admin_routes, url_prefix='/admin') # AI
app.register_blueprint(api_routes, url_prefix='/api')
