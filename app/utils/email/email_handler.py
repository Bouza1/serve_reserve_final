from flask import render_template
from flask_mail import Message
from string import Template
from app import mail
from app.utils.email.cancellation_template import cancellation_template
from app.utils.email.reset_template import reset_template
from app.utils.email.booking_template import booking_created_template
from app.utils.email.account_created_template import account_created_template
from app.utils.email.delete_account_template import delete_account_template

class Email_Handler():
    def __init__(self):
        pass
    
    def reset_email(self, token):
        try:
            message = Message("Reset Password Request", recipients=[token['assigned']])
            message.html = self.format_reset_html(token['id'])
            mail.send(message)
            return True
        except Exception as e:
            print(e)
            return False

    def format_reset_html(self, url_var):
        url = "http://127.0.0.1:5000/reset_link/" + url_var
        return Template(reset_template).safe_substitute(url_1=url)
    
    def cancelation_email(self,booking):
        try:
            message = Message("Booking Cancellation!",  recipients=[booking['user']])
            message.html = self.format_cancellation_email(booking)
            mail.send(message)
        except Exception as e:
            print(e)
    
    def format_cancellation_email(self, booking):
        return Template(cancellation_template).safe_substitute(date=booking['date'], time=booking['time'], court=booking['court'])
    
    def created_booking_email(self, booking):
        message = Message("Booking Created!",  recipients=[booking['user']])
        message.html = self.format_booking_email(booking)
        mail.send(message)

    def format_booking_email(self, booking):
        return Template(booking_created_template).safe_substitute(date=booking['date'], time=booking['time'], court=booking['court'])
    
    def created_account_email(self, account):
        message = Message("Account Created!",  recipients=[account['account']])
        message.html = self.format_acc_create_email(account)
        mail.send(message)

    def format_acc_create_email(self, account):
        return Template(account_created_template).safe_substitute(username=account['account'], password=account['password'])

    def deleted_account_email(self, account):
        message = Message("Account Deleted!",  recipients=[account['account']])
        message.html = self.format_delete_email(account)
        mail.send(message)
    
    def format_delete_email(self, account):
        return Template(delete_account_template).safe_substitute(username=account['account'])