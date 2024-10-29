import mysql.connector as connection 

class db():
    connection = (
    connection.connect(
            host="localhost", 
            port="3309", 
            user = "root", 
            password = "root", 
            database = "expensedb" 
        )
    )
    cursor = connection.cursor()
    print("connected to localhost")
    def __init__(self):
        self.columns = []
        self.table = ""

    def create_connection(self):
        self.connection = (
            connection.connect(
                host="localhost", 
                port="3309", 
                user = "root", 
                password = "root", 
                database = "expensedb" 
            )
        )
        self.cursor = self.connection.cursor()
        print("connected to localhost")

    def insert(self, table="", columns=[], values=[]):
        print(self.table)
        column_str = str(tuple(columns)).replace('\'','')
        values_str = ""
        print(values[len(values)-1])
        for value in values:
            print(value)
            if value != values[len(values)-1]:
                print("y")
                values_str += "%s,"
            else:
                print("n")
                values_str += "%s"

        query = f"insert into {self.table} {column_str} values (" + values_str + ")"
        query = f"insert into {self.table} {column_str} values {str(tuple(values))}"
        print(query)
        print(values)
        self.cursor.execute(
            query,
            # tuple(values)
        )

        print(self.cursor.rowcount, "row inesrted")