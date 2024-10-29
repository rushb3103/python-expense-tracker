from models.main_users import main_users

class user_controller():

    def signup(self):
        main_usersObj = main_users()

        # return 0 
        insert_dict = {
            "username" : "abc",
            "password" : "abc1",
            "dob" : "2002-03-31",
            "mobile" : 23434343454,
            "gender" : "male",
            "first_name" : 'rush',
            "last_name" : "b",
            "email" : "rush@13.cs"
        }
        main_usersObj.insert('',tuple(insert_dict.keys()), tuple(insert_dict.values()))
