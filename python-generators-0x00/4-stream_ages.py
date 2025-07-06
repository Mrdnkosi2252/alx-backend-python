#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    """Generator to yield user ages one by one from the user_data table."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alx_user",  
            password="Davidnkosi12301*",  
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:  # First loop: iterate over query results
            yield row[0]
    except Error as err:
        print(f"Error: {err}")
        yield None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def calculate_average_age():
    """Calculates the average age using the generator without loading all data into memory."""
    total_age = 0
    count = 0
    for age in stream_user_ages():  # Second loop: iterate over yielded ages
        if age is None:
            break
        total_age += age
        count += 1
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age}")
    else:
        print("Average age of users: 0")

if __name__ == "__main__":
   
    calculate_average_age()