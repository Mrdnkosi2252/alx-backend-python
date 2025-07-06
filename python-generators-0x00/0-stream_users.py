#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator to fetch rows one by one from the user_data table."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alx_user",  # Replace with your MySQL username
            password="Davidnkosi12301*",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for key-value pairs
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:  # Single loop to yield rows
            yield row
    except Error as err:
        print(f"Error: {err}")
        yield None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # Example usage
    for user in stream_users():
        if user:
            print(user)