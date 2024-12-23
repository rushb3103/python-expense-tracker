from flask import json
from models.main_users import main_users
from libraries.functions import functions
import hashlib

class user_controller():
    def __init__(self):
        self.functionsObj = functions()

    def signup(self, request):

        username = request.form.get("username", '', str)
        password = request.form.get("password", '', str)
        dob = request.form.get('dob', '', str)
        mobile = request.form.get('mobile', '', str)
        gender = request.form.get('gender', '' , str).lower()
        firstname = request.form.get('firstname', '', str)
        lastname = request.form.get('lastname', '', str)
        email = request.form.get("email", '', str)

        validation_results = {}

        is_valid, message = self.functionsObj.validate_username(username)
        validation_results["username"] = message if not is_valid else "Valid"

        is_valid, message = self.functionsObj.validate_password(password)
        validation_results["password"] = message if not is_valid else "Valid"

        is_valid, message = self.functionsObj.validate_dob(dob)
        validation_results["dob"] = message if not is_valid else "Valid"

        is_valid, message = self.functionsObj.validate_mobile(mobile)
        validation_results["mobile"] = message if not is_valid else "Valid"

        is_valid, message = self.functionsObj.validate_gender(gender)
        validation_results["gender"] = message if not is_valid else "Valid"

        is_valid, message = self.functionsObj.validate_name(firstname)
        validation_results["firstname"] = message if not is_valid else "Valid"

        is_valid, message = self.functionsObj.validate_name(lastname)
        validation_results["lastname"] = message if not is_valid else "Valid"

        is_valid, message = self.functionsObj.validate_email(email)
        validation_results["email"] = message if not is_valid else "Valid"

        for f, result in validation_results.items():
            print(f, result)
            if result != "Valid":
                return self.functionsObj.send_response(0, f"{result}")

        main_usersObj = main_users()
        main_usersObj.where = f"username = '{username}'"
        result = main_usersObj.select()
        if len(result) > 0:
            return self.functionsObj.send_response(0, "Same user Already exists.")
        
        main_usersObj.where = f"mobile = '{mobile}'"
        result = main_usersObj.select()
        if len(result) > 0:
            return self.functionsObj.send_response(0, "Same mobile Already exists.")

        insert_dict = {
            "username" : username ,
            "password" : self.functionsObj.generate_hash(password),
            "dob" : dob,
            "mobile" : mobile,
            "gender" : gender,
            "first_name" : firstname,
            "last_name" : lastname,
            "email" : email
        }
        inserted_record = main_usersObj.insert('',tuple(insert_dict.keys()), tuple(insert_dict.values()))
        if inserted_record > 0:
            return self.functionsObj.send_response(1, "Registration successfull!")
    
    def login(self, request):
        username = request.form.get("username", '', str)
        password = request.form.get("password", '', str)

        main_usersObj = main_users()
        main_usersObj.where = f"username = '{username}' and password = '{password}'"
        records = main_usersObj.select()
        if len(records) > 0:
            return {'status_code':0,'status_message':'Login DOne'}
        return {'status_code':1,'status_message':'Login Failed'}
    
