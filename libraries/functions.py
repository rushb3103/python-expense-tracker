from functools import wraps
import os
import re
from datetime import datetime
import hashlib
import traceback

from flask import jsonify, request
import jwt
from dotenv import load_dotenv
load_dotenv('.env')

class functions():
    def send_response(self, status_code, message, data = []):
        return {
            "status_code" : status_code,
            "status_message" : message,
            "data" : data
        }
    
    def validate_username(self, username:str) -> tuple:
        if not isinstance(username, str) or not str(username).isalnum():
            return False, "Username must be alphanumeric."
        if len(username) < 5 or len(username) > 15:
            return False, "Username must be between 5 to 15 characters."
        return True, ""
    
    def validate_password(self, password:str) -> tuple:
        if len(password) < 8:
            return False, "Length of password must be more than 8."
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain atleast one uppercase letter."
        if not re.search(r'[a-z]', password):
            return False, "Password must contain atleast one lowercase letter."
        if not re.search(r'[0-9]', password):
            return False, "Password must contain atleast one numeric letter."
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain atleast one special character."
        return True, ""
    
    def validate_dob(self, dob:str) -> tuple:
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            return False, "Date of birth must be in the format YYYY-MM-DD."
        
        if dob_date.date() >= datetime.now().date():
            return False, "Current or future DOB is not acceptable."
        
        return True, ""
    
    def validate_mobile(self, mobile:str) -> tuple:
        if not mobile.isdigit():
            return False, "Mobile number must be digit."
        if len(mobile) != 10:
            return False, "Length of mobile number must be 10 digits."
        return True, ""
    
    def validate_gender(self, gender:str) -> tuple:
        if gender.lower() not in ['male', 'female', 'other']:
            return False, "Gender must be either 'Male', 'Female', or 'Other'."
        return True, ""
    
    def validate_name(self, name:str) -> tuple:
        if not name.isalpha():
            return False, f"{name} must contain only alphabetic characters."
        if len(name) == 0:
            return False, "Name cannot be empty."
        return True, ""
    
    def validate_email(self, email:str) -> tuple:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return False, "Email must be in a valid format."
        return True, ""
    
    def validate_transaction_type(self, transaction_type:str) -> tuple:
        if str(transaction_type).lower() not in ["credit", "debit"]:
            return False, "Transaction Must be Credit/Debit"
        return True, ""
    
    def validate_sub_transaction_type(self, sub_transaction_type:str) -> tuple:
        if sub_transaction_type == "":
            return False, "Sub Transaction Must Not be blank."
        return True, ""
    
    def validate_amount(self, amount:float) -> tuple:
        if amount <= 0:
            return False, "Amount must be positive"
        return True, ""
    
    def get_current_datetime(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")


    def generate_hash(self, string:str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(string.encode('utf-8'))
        return sha256.hexdigest()
    

    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            # jwt is passed in the request header
            # if 'x-access-token' in request.headers:
            #     token = request.headers['x-access-token']
            print(request.headers)
            
            return_data = 0
            if request.method != "GET" or str(request.url).find("/user/home") != -1:
                if "Authorization" in request.headers:
                    token = request.headers["Authorization"]
                    token = str(token).split(" ")[-1]
                # return 401 if token is not passed
                if not token:
                    return jsonify({'message' : 'Token is missing !!'}), 401
                
                try:
                    # decoding the payload to fetch the stored details
                    data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms='HS256')
                    return_data = data["id"]
                    # current_user = User.query\
                    #     .filter_by(public_id = data['public_id'])\
                    #     .first()
                except:
                    return jsonify({
                        'message' : 'Token is invalid !!'
                    }), 401
            # returns the current logged in users context to the routes
            return  f(return_data, *args, **kwargs)
    
        return decorated
