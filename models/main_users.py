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


        # def insert(self, values):
            
        #     super.insert()