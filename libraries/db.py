import mysql.connector as connection 

class db():
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
        column_str = str(tuple(columns))
        values_str = ""
        for value in values:
            if value != values[len(values)-1]:
                values_str += "%s,"
            else:
                value += "%s"

        self.cursor.execute(
            f"insert into {self.table} {column_str} values (" + values_str + ")",
            tuple(values)
        )

        print(self.cursor.rowcount, "row inesrted")