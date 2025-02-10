from libraries.db import db

class main_users(db):
    def __init__(self):
        super().__init__()
        self.columns = [
            "username",
            "password",
            "dob",
            "mobile",
            "gender",
            "first_name",
            "last_name",
            "email"
        ]
        self.table = "main_users"

    def get_user_from_id(self, user_id):
        self.fields = "user_name"
        self.where = f"id = {user_id}"
        return self.select()


        # def insert(self, values):
            
        #     super.insert()