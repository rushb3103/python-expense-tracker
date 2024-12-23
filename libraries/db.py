import mysql.connector as connection 


from dotenv import load_dotenv
load_dotenv('.env')


def create_connection():

    import os    
    global db_connection 
    db_connection = (
    connection.connect(
            host=str(os.getenv("DATABASE_HOST")), 
            port=int(os.getenv("DATABASE_PORT")), 
            user = str(os.getenv("DATABASE_USER")), 
            password = str(os.getenv("DATABASE_PASSWORD")), 
            database = str(os.getenv("DATABASE_NAME"))
        )
    )
    global cursor 
    cursor = db_connection.cursor()
    print("connected to localhost")

create_connection()
class db():
    def __init__(self):
        self.columns = []
        self.table = ""
        self.fields = "*"
        self.where = ""
        self.join = ""
        self.connection = db_connection
        self.cursor = cursor
        # print("connected to localhost")

    # def create_connection(self):

    def insert(self, table="", columns=[], values=[]):
        print(self.table)
        column_str = str(tuple(columns)).replace('\'','')
        values_str = ""
        print(values[len(values)-1])
        for value in values:
            print(value)
            if value != values[len(values)-1]:
                values_str += "%s,"
            else:
                values_str += "%s"

        query = f"insert into {self.table} {column_str} values (" + values_str + ")"
        query = f"insert into {self.table} {column_str} values {str(tuple(values))}"
        print(query)
        print(values)
        self.cursor.execute(
            query,
            # tuple(values)
        )
        self.connection.commit()
        print(self.cursor.rowcount, "row inesrted")
        return self.cursor.rowcount

    def insert_dict(self, insert_dict : dict):
        return self.insert(tuple(insert_dict.keys()), tuple(insert_dict.values()))
        # pass

    def select(self, execute_dict=False):
        query = f"""
            select {self.fields} from {self.table} {self.join} where {self.where}
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result