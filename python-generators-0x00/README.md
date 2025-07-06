# Python Generators - Task 0: Getting Started with Python Generators

## Overview
This directory contains a Python script (`seed.py`) that demonstrates the use of generators to stream data from a MySQL database. The script sets up the `ALX_prodev` database, creates a `user_data` table, populates it with sample data from `user_data.csv`, and provides a generator to stream rows.

## Files
- `seed.py`: Python script with database connection, table creation, data insertion, and a row-streaming generator.
- `user_data.csv`: Sample CSV file with user data (name, email, age).
- `README.md`: This file.

## Setup
1. Install MySQL Connector for Python:
   ```bash
   python.exe -m pip install mysql-connector-python