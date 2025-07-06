#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

def paginate_users(page_size, offset):
    """Fetches a specific page of users from the user_data table."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alx_user",  # Replace with your MySQL username
            password="Davidnkosi12301*",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        return cursor.fetchall()
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def lazy_paginate(page_size):
    """Generator to lazily load paginated data from the user_data table."""
    offset = 0
    while True:
        users = paginate_users(page_size, offset)
        if not users:
            break
        for user in users:  # Single loop to yield users
            yield user
        offset += page_size

if __name__ == "__main__":
    # Example usage
    page_size = 3
    for user in lazy_paginate(page_size):
        print(user)