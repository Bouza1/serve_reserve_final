from app import app, bcrypt
from app.user.user_class import User
from app.utils.day import Day
from flask import Blueprint, jsonify, request, session
from app.admin.admin_class import Admin 

admin = Admin()
user = User()

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/times_booked', methods=['PUT'])
def times_booked():
    ''' Returns the Times available/booked for a given court and date '''
    if request.is_json:
        json_obj = request.get_json()
        day = Day(json_obj['date'],json_obj['court'])
        if session['role'] == 'user':
            return {"times": day.check_for_day()}
        elif session['role'] == 'admin':
            return admin.format_times(day.check_for_day())
    else:
        return {"message":"No Times Available"}
    
@api_routes.route('/handle_booking', methods=['GET', 'PUT'])
def handle_booking():
    ''' Handles Booking And Cancellation Requests '''
    if request.is_json:
        if session['role'] == 'user':
            return user.handle_booking(request.get_json())
        elif session['role'] == 'admin':
            return admin.handle_booking(request.get_json())



@api_routes.route('/search_user_email', methods=['POST'])
def return_user_email():
    ''' Returns a users details from a given email address '''
    if session.get('role') == "admin" and request.is_json:
        json_obj = request.get_json()
        return admin.return_user_search_email(json_obj['user'])

@api_routes.route('/return_users',  methods=['GET'])
def return_users():
    ''' Returns all emails'''
    if session['role'] == 'admin':
        return admin.return_all_users_emails()
