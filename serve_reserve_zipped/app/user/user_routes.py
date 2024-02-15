from app.user.user_class import User
from flask import Blueprint, render_template, session, request, redirect, url_for
from app.utils.security import Sec
from app import app, bcrypt


user_routes = Blueprint('user_routes', __name__)

sec = Sec()
user = User()

@user_routes.route('/dashboard')
def user_dashboard():
    ''' Returns user dashboard dependent on being logged into the system '''
    if not session.get('logged_in'):
        return render_template("login.html", message='{"type":"danger", "title":"Access Denied", "message":"To enter the user dashboard please login or create an account."}')
    else:
       return render_template('user_dashboard.html', user=user.return_user_object(sec.enc(session['username'])))

@user_routes.route('/update_profile', methods=['POST'])
def update_profile():
      ''' Handles the updating of user profile details'''
      if request.method == 'POST':
            changed = user.update_profile(request.form)
            if session.get('testing') == True:
                return changed['message']
            if changed['updated'] == True:
                if session.get('role') == "admin":
                    return render_template('admin_dashboard.html', user = user.return_user_object(sec.enc(session['username'])), message='{"type":"success", "title":"Account Profile", "message":"%s"}' % changed['message'])
                else:
                    return render_template('user_dashboard.html', user = user.return_user_object(sec.enc(session['username'])), message='{"type":"success", "title":"Account Profile", "message":"%s"}' % changed['message'])
            else:
                if session.get('role') == "admin":
                    return render_template('admin_dashboard.html', user = user.return_user_object(sec.enc(session['username'])), message='{"type":"danger", "title":"Account Profile", "message":"%s"}' % changed['message'])
                else:
                    return render_template('user_dashboard.html', user = user.return_user_object(sec.enc(session['username'])), message='{"type":"danger", "title":"Account Profile", "message":"%s"}' % changed['message'])
                
    
@user_routes.route('/change_password', methods=['POST'])
def change_password():
     ''' Handles password change requests when initiated from the main menu '''
     if request.method == 'POST':
        changed = user.update_password(bcrypt.generate_password_hash(request.form.get('new_pword')).decode('utf-8'), sec.enc(session['username']))
        if changed == True:
            if session.get('role') == 'admin':
                return render_template("admin_dashboard.html", user=user.return_user_object(sec.enc(session['username'])), message = '{"type":"success", "title":"Password Change", "message":"Password Changed Successfully!"}')
            else:
                return render_template("user_dashboard.html", user=user.return_user_object(sec.enc(session['username'])), message = '{"type":"success", "title":"Password Change", "message":"Password Changed Successfully!"}')
        else:
            if session.get('testing'):
                return render_template("login.html", message = '{"type":"danger", "title":"Password Change", "message":"Error! The Request To Change Your Password Has Failed!"}')
            else:
                return render_template("user_dashboard.html", user=user.return_user_object(sec.enc(session['username'])), message = '{"type":"danger", "title":"Password Change", "message":"Error! The Request To Change Your Password Has Failed!"}')

  

@user_routes.route('/delete_account', methods=['POST'])
def delete_account():
    ''' Handles the deletion of acocunts '''
    if request.method == 'POST' and session.get('role') == 'user':
        wiped = user.wipe_account(request.form.get('delete_pword'))
        if wiped['deleted'] == True:
            session.clear()
            return render_template('login.html', message='{"type":"danger", "title":"Account Deletion", "message":"Your Account Has Been Succesfully Deleted"}')
        else:
            if session.get('testing') == True:
                return wiped['message']
            else:
                return render_template('user_dashboard.html', user=user.return_user_object(sec.enc(session['username'])), message='{"type":"danger", "title":"Account Deletion", "message":"%s"}' % wiped['message'])

