from app.auth.auth import Authenticate
from app.utils.db import DBHANDLER
from app.utils.email.email_handler import Email_Handler
from app.utils.security import Sec
from datetime import datetime
from app import mail, bcrypt
from flask import session

class Admin:
        
    def __init__(self):
        self.sec = Sec()
    
    def return_all_users_emails(self):
        ''' Returns a list of all users emails'''
        db = DBHANDLER()
        newSec = Sec()
        user_list = db.return_all("SELECT * FROM users")
        holder=[]
        for user in user_list:
            holder.append(newSec.dec(user[0]))
        return {"emails":holder}
    
    def return_user_search_email(self, email):
        ''' Returns a user for a given email '''
        db = DBHANDLER()
        user = db.search_return_one("SELECT * FROM users WHERE id = %s", (self.sec.enc(email),))
        return {"user":self.format_user_returned(user)}
    
    def format_user_returned(self, user):
        ''' Formats the response from the database into a user object '''
        newSec = Sec()
        role = ""
        if newSec.dec(user[3]) == 'admin':
            role = "Club Admin"
        else:
            role = "Club Member"
        return {
                "username":newSec.dec(user[0]), 
                "firstname":newSec.dec(user[1]),
                "lastname":newSec.dec(user[2]),
                "role":role, 
                "housenum":self.check_for_null(user[4]),
                "street":self.check_for_null(user[5]),
                "town":self.check_for_null(user[6]),
                "postcode":self.check_for_null(user[7]),
                "phonenumber":self.check_for_null(user[8])
                }
    
    def check_for_null(self, element):
        if element == None or "" or 0 or False:
            return ""
        else:
            return self.sec.dec(element)
        
    def format_times(self, times):
        ''' Decrypts email addresses within the times[]'''
        newSec = Sec()
        arr = [times[0], times[1]]
        for i in range(2, len(times)):
            if times[i] == '0':
                arr.append('0')
            else:
                arr.append(newSec.dec(times[i]))
        return {"times":arr}
    
    
    def handle_booking(self, booking):
        ''' Handles both cancellations and bookings. Returns a message object so the client side can display notification '''
        db = DBHANDLER()
        numbers = {"7": "seven","8": "eight","9": "nine","10": "ten","11": "eleven","12": "twelve","13": "thirteen","14": "fourteen","15": "fifteen","16": "sixteen","17": "seventeen","18": "eighteen","19": "nineteen"}
        if str(booking['time']) in numbers:
            sql_statement = f"UPDATE {booking['court']} SET {numbers[str(booking['time'])]} = %s WHERE day = %s"
        else:
            return {"type":"danger", "title":"Booking Error!",  "message":"This court opening hours are from 7:00 - 19:00, Please book accordingly"}
        if self.sec.is_email(booking['user']) == False:
            return {"type":"danger", "title":"Booking Error!",  "message":"InvaLid Email, If The Error Persists Please Call The Club To Book!"}
        try:
            if booking['cancel'] == True:

                db.insert_into(sql_statement, ("0", booking['date']))
                if session.get('testing') == True:
                    return {"type":"warning", "title":"Booking Cancelled!",  "message": self.return_booking_message(booking)}
                email = Email_Handler()
                email.cancelation_email(self.return_booking_email_obj(booking))
                return {"type":"warning", "title":"Booking Cancelled!",  "message": self.return_booking_message(booking)}
            else:
                db.insert_into(sql_statement, (self.sec.enc(booking['user']), booking['date']))
                if session.get('testing') == True:
                    return {"type":"success", "title":"Booking Complete!",  "message":self.return_booking_message(booking)}
                email = Email_Handler()
                email.created_booking_email(self.return_booking_email_obj(booking))
                return {"type":"success", "title":"Booking Complete!",  "message":self.return_booking_message(booking)}
        except Exception as e:
            return {"type":"danger", "title":"Booking Error!",  "message":"Failed To Complete Booking, If The Error Persists Please Call The Club To Book!"}

    def return_booking_message(self, booking):
        ''' Formats the booking into a more user friendly statememnt ready for the client side to display inside the notification '''
        courts = {"grass_one":"Grass Court One", "grass_two":"Grass Court Two", "clay_one":"Clay Court"}
        timeEnd = int(booking['time'])+1
        endTime = str(timeEnd) +":00."
        startTime = str(booking['time']) + ":00"
        fullTimeStr = f"{startTime} - {endTime}"
        if booking['cancel'] == False:
            return f'{courts[booking["court"]]} \n {self.format_date(booking["date"])} \n {fullTimeStr} \n {booking["user"]}'
        else:
            return f'{courts[booking["court"]]} \n {self.format_date(booking["date"])} \n {fullTimeStr} \n {booking["user"]}'
        
    def return_booking_email_obj(self, booking):
        ''' Formats the booking into a more user friendly statememnt ready for sending via email '''
        courts = {"grass_one":"Grass Court One", "grass_two":"Grass Court Two", "clay_one":"Clay Court"}
        timeEnd = int(booking['time'])+1
        endTime = str(timeEnd) +":00."
        startTime = str(booking['time']) + ":00"
        fullTimeStr = f"{startTime} - {endTime}"
        return {"court":" " + courts[booking['court']], "date":self.format_date(booking['date']), "time":fullTimeStr[:-1], "user":booking['user']}


    def format_date(self,input_date):
        ''' Takes a date and returns it in yyyy-mm-dd format'''
        date_object = datetime.strptime(input_date, "%Y-%m-%d")
        day_of_week = date_object.strftime("%A")
        formatted_date = date_object.strftime("%dth %B")
        return f"{day_of_week} {formatted_date}"
    
    def create_account(self, form):
        ''' Handles the creation of both administrator or club member accounts. '''
        newSec = Sec()
        newAuth = Authenticate()
        db = DBHANDLER()
        valid = self.validate_account_inputs(form)
        if valid == True:
            user_exists = newAuth.check_user_exists(newSec.enc(form.get('email')))
            if user_exists == True:
                return {"created":False, "message":"An account with this username already exists!"}
            elif user_exists == False:
                secure_password = newSec.generate_secure_password()
                hashed_password = bcrypt.generate_password_hash(secure_password).decode('utf-8')
                if session.get('testing') == True:
                    print("Skipping Email")
                else:
                    email = Email_Handler()
                    email.created_account_email({"account":form.get('email'),"password":secure_password})
                try:
                    db.insert_into("INSERT INTO security (id, password) VALUES (%s, %s)", (self.sec.enc(form.get('email')), hashed_password))
                    db.insert_into("INSERT INTO users (id, first_name, last_name, role) VALUES (%s, %s, %s, %s)",(self.sec.enc(form.get('email')), self.sec.enc(form.get('firstname')), self.sec.enc(form.get('lastname')), self.sec.enc(form.get('role'))))
                    return {"created":True, "message":"Account Created Succesfully, Please Direct User To Their Emails."}
                except Exception as e:
                    return {"created":False, "message":str(e)}
            else:
                return {"created":False, "message":user_exists['error']}
        else:
            return {"created":False, "message":valid['message']}
        
    def validate_account_inputs(self, form):
        if len(form.get('firstname')) < 3 or len(form.get('firstname')) > 150:
            return{'message':"Invalid First Name, Please enter a first name between 3 - 150 characters in length"}
        if len(form.get('lastname')) < 3 or len(form.get('lastname')) > 150 or form.get('lastname') == "":
            return{'message':"Invalid Surname, Please enter surname between 3 - 150 characters in length"}
        if self.sec.is_email(form.get('email')) == False:
            return{'message':"Invalid Email Address, Please Try Again"}
        if form.get('role') != 'user' and form.get('role') != 'admin':
            return{'message':"Invalid Role, Please Select User or Admin"}
        
        return True


    def delete_users_account(self, form):
        ''' Handles the deletion of user accounts '''
        newAuth = Authenticate()
        auth_token = newAuth.get_user_security(self.sec.enc(session['username']), form.get('delete_pword'))
        user_exists = newAuth.check_user_exists(self.sec.enc(form.get('email_delete')))

        if user_exists == False:
            return {"deleted":False, "message":"Error Deleting Account, Incorrect Email!"}
        
        if auth_token['token'] == True:

            try:
                db = DBHANDLER()   
                db.insert_into("DELETE FROM users WHERE id = %s", (self.sec.enc(form.get('email_delete')),))
                db.insert_into("DELETE FROM resets WHERE assigned = %s", (self.sec.enc(form.get('email_delete')),))
                db.insert_into("DELETE FROM security WHERE id = %s", (self.sec.enc(form.get('email_delete')),))
                if session.get('testing') == True:
                    return {"deleted":True, "message":"Account Deleted!"}
                else:
                    email = Email_Handler()
                    email.deleted_account_email({"account":form.get('email_delete')})
                    return {"deleted":True, "message":"Account Deleted!"}
            except Exception as e:               
                return {"deleted":False, "message":e}
        else:
             return {"deleted":False, "message":"Incorrect Password!"}