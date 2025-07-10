import mysql.connector
from mysql.connector import Error

class ExecuteQuery:
    def __init__(self, host, database, user, password, query, param):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.query = query
        self.param = param
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute(self.query, (self.param,))
            self.results = self.cursor.fetchall()
            return self.results
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection and cursor closed.")

if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "database": "alx_prodev",
        "user": "alx_user",
        "password": "Davidnkosi12301*"
    }

    
    query = "SELECT * FROM user_data WHERE age > %s"

    with ExecuteQuery(**db_config, query=query, param=25) as results:
        if results:
            print("Query results:")
            for row in results:
                print(row)