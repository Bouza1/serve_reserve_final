from app.auth.auth import Authenticate
from app.auth.reset import Reset_Token
from app.utils.email.email_handler import Email_Handler
from flask import session, redirect, url_for, render_template
from app.utils.db import DBHANDLER
from app.utils.security import Sec
from app import app, bcrypt
from datetime import datetime

class User:
        
    def __init__(self):
        self.sec = Sec()
        
    def login(self, username):
        ''' Handles the login process for both administrators and club members '''
        self.user_obj = self.return_user_object(self.sec.enc(username))
        session['logged_in'] = True
        session['username'] = username
        session['firstname'] = self.user_obj['firstname']
        session['lastname'] = self.user_obj['lastname']
        session['role'] = self.user_obj['role']
        if session.get('role') == "admin":
            return redirect(url_for('admin_routes.admin_dashboard'))
        else:
            return redirect(url_for('user_routes.user_dashboard'))
        
    def return_user_object(self, username):
        ''' Decrypts the encrypted user details stored within the database and returns a uniform object '''
        db = DBHANDLER()
        statement = "SELECT * FROM users WHERE id = %s"
        self.user = db.search_return_one(statement,(username,))
        return {
            "username":self.user[0], 
            "email":self.sec.dec(self.user[0]), 
            "firstname":self.sec.dec(self.user[1]),
            "lastname":self.sec.dec(self.user[2]),
            "role":self.sec.dec(self.user[3]), 
            "housenum":self.check_for_null(self.user[4]),
            "street":self.check_for_null(self.user[5]),
            "town":self.check_for_null(self.user[6]),
            "postcode":self.check_for_null(self.user[7]),
            "phonenumber":self.check_for_null(self.user[8])
            }
    
    def check_for_null(self, element):
        if element == None or "" or 0 or False:
            return ""
        else:
            return self.sec.dec(element)
            

    def logout(self):
        ''' Handles the logout '''
        session.clear()
        return redirect(url_for('auth_routes.login_page'))
    
    def register_user(self, form, password):
        ''' Encrypts & inserts new user details into the database '''
        valid = self.validate_account_inputs(form)
        if valid == True:
            try:
                db = DBHANDLER()
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                db.insert_into("INSERT INTO security (id, password) VALUES (%s, %s)", (self.sec.enc(form.get('email')), hashed_password))
                db.insert_into("INSERT INTO users (id, first_name, last_name, role) VALUES (%s, %s, %s, %s)",(self.sec.enc(form.get('email')), self.sec.enc(form.get('fname')), self.sec.enc(form.get('fname')), self.sec.enc(form.get('role'))))
                return render_template('login.html', message='{"type":"success", "title":"Account Creation",  "message":"Account Created!"}')
            except:
                return render_template('register.html', message='{"type":"danger", "title":"Registration Error", "message":"Error! Please Try Again If the Error Persists Please Contact The Site Administrators"}' )
        else:
            return render_template('login.html', message='{"type":"danger", "title":"Account Creation",   "message":"%s"}' % valid['message'])
        

    def validate_account_inputs(self, form):
        if len(form.get('fname')) < 3 or len(form.get('fname')) > 150 or form.get('fname') == "":
            return{'message':"Invalid First Name, Please enter a first name between 3 - 150 characters in length"}
        if len(form.get('lname')) < 3 or len(form.get('lname')) > 150 or form.get('lname') == "":
            return{'message':"Invalid Surname, Please enter surname between 3 - 150 characters in length"}
        if self.sec.is_email(form.get('email')) == False:
            return{'message':"Invalid Email Address, Please Try Again"}
        if form.get('role') != 'user' and form.get('role') != 'admin':
            return{'message':"Invalid Role, Please Select User or Admin"}
        
        return True
        

    def send_reset_email(self, email_adress):
        ''' Handles the reset password email processs '''
        rec = Reset_Token(email_adress)
        rec.spend_previous_tokens(rec.token['E']['assigned'])
        rec.insert_token()
        email = Email_Handler()
        sent = email.reset_email(rec.token['D'])
        if sent == True:
            return render_template('login.html', message='{"type":"success", "title":"Reset Password",  "message":"Please Check Your Email For Further Instructions"}') 
        else:
             return render_template('login.html', message='{"type":"danger", "title":"Reset Password",  "message":"Error!"}')
        
    def valid_reset_link(self, token):
        ''' Checks if a reset token is presetn in the database '''
        db = DBHANDLER()
        return db.search_return_one("SELECT * FROM resets WHERE id = %s AND token = '0'",(token,))

    def change_password_exterminate_token(self, token, password):
        ''' Handles the process of changing a password via a reset token and invalidating the token after use '''
        rec = Reset_Token("dummy")
        valid_token = self.valid_reset_link(token)
        try:
            self.update_password(bcrypt.generate_password_hash(password).decode('utf-8'), valid_token[2])
            rec.spend_token(token)
            return render_template('login.html', message='{"type":"success", "title":"Reset Password",  "message":"Please Login Using Your New Password!"}') 
        except Exception as e:
            return render_template('login.html', message='{"type":"danger", "title":"Reset Password",  "message":"Error!"}')

    def update_password(self, password, user):
        ''' Handles the changing of user password from the main menu '''
        newAuth = Authenticate()
        if newAuth.check_user_exists(user) == True:
            try:
                db = DBHANDLER()
                db.insert_into("UPDATE security SET password = %s WHERE id = %s", (password, user))
                return True
            except Exception as e:
                return False
        else:
            return False
        
    def update_profile_checks(self, form):
        if len(form.get('firstname')) < 3 or len(form.get('firstname')) > 150:
            return{'message':"Invalid First Name, Please enter a first name between 3 - 150 characters in length"}
        
        if len(form.get('lastname')) < 3 or len(form.get('lastname')) > 150 or form.get('lastname') == "":
            return{'message':"Invalid Surname, Please enter surname between 3 - 150 characters in length"}
        
        if len(form.get('housenum')) > 40:
            return{'message':"Invalid House Number, Please enter House Number no more than 150 characters in length"}
        
        if form.get('street') != "":
            if len(form.get('street')) > 150 or len(form.get('street')) < 5:
                return{'message':"Invalid Street Address, Please enter Street Address no more than 150 characters in length"}
        
        if form.get('town') != "":
            if len(form.get('town')) > 90 or len(form.get('town')) < 5:
                return{'message':"Invalid Town Address, Please enter a town no more than 90 characters in length"}
            
        if form.get('postcode') != "":
            if len(form.get('postcode')) > 10 or Sec.is_uk_postcode(form.get('postcode')) == False:
                return{'message':"Invalid PostCode, Please enter a valid postcode. For Example DT117HD or DT11 7HD"}

        if form.get('phonenum') != "":
            if  Sec.is_uk_phone_number(form.get('phonenum'))  == False:
                return{'message':"Invalid Phone Number, Please enter a valid UK Phone Number"}

        if self.sec.is_email(form.get('hidden_email')) == False:
            return{'message':"Invalid Email Address, Please Contact The Club Directly"}
        
        
        return True

    def update_profile(self,form):
        ''' Handles the encrption and insertion of updated user profile details '''
        changed = self.update_profile_checks(form)
        if changed == True:
            firstname = self.sec.enc(form.get('firstname'))
            lastname = self.sec.enc(form.get('lastname'))
            housenum = self.sec.enc(form.get('housenum'))
            street = self.sec.enc(form.get('street'))
            town = self.sec.enc(form.get('town'))
            postcode = self.sec.enc(form.get('postcode'))
            phonenum = self.sec.enc(form.get('phonenum'))
            email = self.sec.enc(form.get('hidden_email'))
            role = self.sec.enc(session['role'])
            update_query = "UPDATE users SET first_name = %s, last_name = %s, role = %s, house_num = %s, street = %s, town = %s, postcode = %s, phone_num = %s WHERE id = %s"
            db = DBHANDLER()
            db.insert_into(update_query, (firstname, lastname, role, housenum, street, town, postcode, phonenum, email))
            return {"updated":True, "message":"Profile Updated Successfully!"}
        else:
            return {"updated":False, "message":changed['message']}
      
    def handle_booking(self, booking):
        ''' Handles the cancelation and booking process for club members'''
        db = DBHANDLER()
        numbers = {"7": "seven","8": "eight","9": "nine","10": "ten","11": "eleven","12": "twelve","13": "thirteen","14": "fourteen","15": "fifteen","16": "sixteen","17": "seventeen","18": "eighteen","19": "nineteen"}
        if str(booking['time']) in numbers:
            sql_statement = f"UPDATE {booking['court']} SET {numbers[str(booking['time'])]} = %s WHERE day = %s"
        else:
             return {"type":"danger", "title":"Booking Error!",  "message":"This court opening hours are from 7:00 - 19:00, Please book accordingly"}
        try:
            if booking['cancel'] == True:
                db.insert_into(sql_statement, ("0", booking['date']))
                return {"type":"warning", "title":"Booking Cancelled!",  "message": self.return_booking_message(booking)}
            else:
                if self.sec.is_email(self.sec.dec(booking['user'])):
                    db.insert_into(sql_statement, (booking['user'], booking['date']))
                    return {"type":"success", "title":"Booking Complete!",  "message":self.return_booking_message(booking)}
                else:
                    return {"type":"danger", "title":"Booking Error!",  "message": "Please contact the club"}
        except Exception as e:
            return {"type":"danger", "title":"Booking Error!",  "message":"Failed To Complete Booking, If The Error Persists Please Call The Club To Book!"}

    def return_booking_message(self, booking):
        ''' Formats a booking message ready for notications or emails '''
        courts = {"grass_one":"Grass Court One", "grass_two":"Grass Court Two", "clay_one":"Clay Court"}
        timeEnd = int(booking['time'])+1
        endTime = str(timeEnd) +":00."
        startTime = str(booking['time']) + ":00"
        if booking['cancel'] == False:
            return f"Court: {courts[booking['court']]} \n Date: {self.format_date(booking['date'])}. \n Time: {startTime} - {endTime}"
        else:
            return f"Court: {courts[booking['court']]} \n Date: {self.format_date(booking['date'])}. \n Time: {startTime} - {endTime}"

    # =============================== START AI ===============================
    def format_date(self,input_date):
        # Convert the input date string to a datetime object # AI
        date_object = datetime.strptime(input_date, "%Y-%m-%d") # AI
        # Get the day of the week and format the date
        day_of_week = date_object.strftime("%A") # AI
        formatted_date = date_object.strftime("%dth %B") # AI
        return f"{day_of_week} {formatted_date}" # AI
    # =============================== END AI ===============================

    def wipe_account(self, password):
        # Verify the user is using correct authentication detials and then handles deletion of acocunt
        newAuth = Authenticate()
        userExists = newAuth.get_user_security(self.sec.enc(session['username']), password)
        if userExists['token'] == True:
            try:
                db = DBHANDLER()
                db.insert_into("DELETE FROM users WHERE id = %s", (self.sec.enc(session['username']),))
                db.insert_into("DELETE FROM resets WHERE assigned = %s", (self.sec.enc(session['username']),))
                db.insert_into("DELETE FROM security WHERE id = %s", (self.sec.enc(session['username']),))
                return {"deleted":True, "message":"Account Deleted!"}
            except Exception as e:               
                return {"deleted":False, "message":"Error Deleting Account, Please Contact The Club To Initiate Account Deletion On Your Behalf"}
        else:
            if newAuth.check_user_exists(self.sec.enc(session['username'])) == True:
                 return {"deleted":False, "message":"Error Deleting Account, Incorrect Password!"}           
            return {"deleted":False, "message":"Error Deleting Account, Incorrect Email!"}

