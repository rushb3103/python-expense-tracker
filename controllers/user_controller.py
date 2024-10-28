from models.main_users import main_users

class user_controller():

    def signup(self):
        main_usersObj = main_users()

        return 0 
        main_usersObj.insert()
