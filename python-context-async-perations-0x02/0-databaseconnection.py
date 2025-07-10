import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL Database: {e}")
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "database": "alx_prodev",
        "user": "alx_user",
        "password": "Davidnkosi12301*"
    }

    with DatabaseConnection(**db_config) as connection:
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user_data")
            rows = cursor.fetchall()
            print("Query results:")
            for row in rows:
                print(row)
            cursor.close()