#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Generator to fetch rows from the user_data table in batches."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alx_user",  
            password="Davidnkosi12301*",  
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)  #
        cursor.execute("SELECT * FROM user_data")
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows
    except Error as err:
        print(f"Error: {err}")
        yield None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def batch_processing(batch_size):
    """Generator to process batches and filter users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):  # First loop: iterate over batches
        if batch is None:
            break
        filtered_batch = [user for user in batch if user['age'] > 25]  # Second loop: list comprehension
        if filtered_batch:
            yield filtered_batch

if __name__ == "__main__":
    # Example usage
    batch_size = 3
    for batch in batch_processing(batch_size):
        print(f"Batch: {batch}")
