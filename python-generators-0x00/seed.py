#!/usr/bin/python3
import mysql.connector
import csv
import uuid
from datetime import datetime

def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alx_user",
            password="Davidnkosi12301*"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
        print("Database ALX_prodev created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(
    host="localhost",
    user="alx_user",
    password="Davidnkosi12301*",
    database="ALX_prodev"
)

        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Creates the user_data table if it does not exist with required fields."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,

                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(10, 2) NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX idx_user_id ON user_data(user_id)")
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, csv_file):
    """Inserts data into the database if it does not exist."""
    try:
        cursor = connection.cursor()
        # Check if table is empty
        cursor.execute("SELECT COUNT(*) FROM user_data")
        if cursor.fetchone()[0] == 0:
            with open(csv_file, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header
                for row in csv_reader:
                    user_id = str(uuid.uuid4())  # Converts UUID to a string format (e.g. 'f9ba2e8c-...')
  
                    name, email, age = row
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, float(age)))
                connection.commit()
            print(f"Data inserted from {csv_file}")
        else:
            print("Data already exists in user_data table")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")

def stream_users(connection):
    """Generator to stream rows from the user_data table one by one."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")
        yield None

if __name__ == "__main__":
    # Example usage
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()
        conn = connect_to_prodev()
        if conn:
            create_table(conn)
            insert_data(conn, "user_data.csv")
            # Example of using the generator
            for user in stream_users(conn):
                if user:
                    print(user)
            conn.close()