from app.admin.admin_class import Admin
from app.user.user_class import User
from app.utils.security import Sec
from flask import Blueprint, render_template, session, request
from app import app, sec

admin_routes = Blueprint('admin_routes', __name__)
user = User()
admin = Admin()

@admin_routes.route('/dashboard')
def admin_dashboard():
    ''' Returns the Admin Dashboard '''
    if session.get('role') == "admin":
        return render_template('admin_dashboard.html', user = user.return_user_object(sec.enc(session['username'])))
    else:
        return render_template("login.html", message='{"type":"danger", "title":"Access Denied", "message":"To enter please login using your credentials."}')
    
@admin_routes.route('/create_user', methods=['POST'])
def create_user():#
    ''' Handles User Creation'''
    if request.method == 'POST':
        created = admin.create_account(request.form)
        if session.get('testing') == True:
            return created['message']
        if created['created'] == True:
            return render_template('admin_dashboard.html', user = user.return_user_object(sec.enc(session['username'])), message='{"type":"success", "title":"Account Creation", "message":"%s"}' % created['message'])
        elif created['created'] == False:
            return render_template('admin_dashboard.html', user = user.return_user_object(sec.enc(session['username'])), message='{"type":"danger", "title":"Account Creation", "message":"%s"}' % created['message'])

@admin_routes.route('/delete_account', methods=['POST'])
def delete_account():
    if request.method == 'POST':
        wiped = admin.delete_users_account(request.form)
        if wiped['deleted'] == True:
            return render_template('admin_dashboard.html', user = user.return_user_object(sec.enc(session['username'])), message='{"type":"success", "title":"Account Deleted", "message":"%s"}' % wiped['message'])
        elif wiped['deleted'] == False:
            return render_template('admin_dashboard.html', user = user.return_user_object(sec.enc(session['username'])), message='{"type":"Danger", "title":"Account Deleted", "message":"%s"}' % wiped['message'])

