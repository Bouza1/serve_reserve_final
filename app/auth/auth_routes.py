from app import app, bcrypt
from app.auth.auth import Authenticate
from app.user.user_class import User
from app.utils.security import Sec
from flask import Blueprint, render_template, request

auth_routes = Blueprint('auth_routes', __name__)

auth = Authenticate()
user = User()
sec = Sec()

@auth_routes.route('/')
def login_page():
    ''' Returns the login page '''
    return render_template('login.html')

@auth_routes.route('/login', methods=['POST'])
def login():
    ''' Handles the authentiation process when logging in '''
    if request.method == 'POST':
        auth_token = auth.get_user_security(sec.enc(request.form['username']), request.form['password'])
        if 'error' not in auth_token: 
            return user.login(request.form['username'])
        elif auth_token['error']:
            return render_template('login.html', message='{"type":"danger", "title":"Login Attempt", "message":"%s"}' % auth_token['error'])
        

@auth_routes.route('/reset_password_request', methods =['POST'])
def reset_password():
    ''' Handles the reset password process '''
    if request.method == 'POST':
        auth_token = auth.check_user_exists(sec.enc(request.form.get('username_reset')))
        if auth_token == False:
            return render_template('login.html', message='{"type":"danger", "title":"Password Reset", "message":"No Account Exists"}')
        elif auth_token == True:
            return user.send_reset_email(request.form.get('username_reset'))


@auth_routes.route('/register')
def register_page():
    ''' Returns the Register Page '''
    return render_template('register.html')


@auth_routes.route('/register_user', methods=['POST'])
def register_user():
    ''' Handles the registration of new club members '''
    if request.method == 'POST':
        auth_token = auth.check_user_exists(sec.enc(request.form.get('email')))
        if auth_token == False:
            return user.register_user(request.form, request.form.get('password'))
        elif auth_token == True:
            return render_template('register.html', message='{"type":"danger", "title":"Registration Error", "message":"Username Already Exists"}')


@auth_routes.route("/reset_link/<reset_id>", methods=['GET'])
def reset_link(reset_id):
    ''' Verifies the dynamic vairable <reset_id> exists within the database before granting/denying access '''
    token = sec.enc(reset_id)
    if user.valid_reset_link(token) != None:
        return render_template('reset.html', token=token)
    else:
        return render_template('login.html', message='{"type":"danger", "title":"Password Reset",  "message":"Invalid Reset Token!"}')
    

@auth_routes.route("/change_password", methods=['POST'])
def change_password():
    ''' Handles the changing of password from reset_link/<reset_id> pages '''
    if request.method == 'POST':
        return user.change_password_exterminate_token(request.form.get('token'), request.form.get('password'))


@auth_routes.route("/logout")
def logout():
    ''' Handles the logging out of users '''
    return user.logout()