from flask import json
from models.main_users import main_users

class user_controller():

    def signup(self, request):

        username = request.form.get("username", '', str)
        password = request.form.get("password", '', str)
        dob = request.form.get('dob', '', str)
        mobile = request.form.get('mobile', 0, int)
        gender = request.form.get('gender', '' , str)
        firstname = request.form.get('firstname', '', str)
        lastname = request.form.get('lastname', '', str)
        email = request.form.get("email", '', str)

        # return 0 
        insert_dict = {
            "username" : username ,
            "password" : password,
            "dob" : dob,
            "mobile" : mobile,
            "gender" : gender,
            "first_name" : firstname,
            "last_name" : lastname,
            "email" : email
        }
        main_usersObj = main_users()
        inserted_record = main_usersObj.insert('',tuple(insert_dict.keys()), tuple(insert_dict.values()))
        return {'status_code':0,'status_message':'User Inserted'}
    
    def login(self, request):
        username = request.form.get("username", '', str)
        password = request.form.get("password", '', str)

        main_usersObj = main_users()
        main_usersObj.where = f"username = '{username}' and password = '{password}'"
        records = main_usersObj.select()
        if len(records) > 0:
            return {'status_code':0,'status_message':'Login DOne'}
        return {'status_code':1,'status_message':'Login Failed'}
