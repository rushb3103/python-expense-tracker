import re
from datetime import datetime
import hashlib

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
    
    def generate_hash(self, string:str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(string.encode('utf-8'))
        return sha256.hexdigest()
