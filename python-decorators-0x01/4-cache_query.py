import time
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
        return result
    return wrapper

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            return query_cache[query]
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")


    users_again = fetch_users_with_cache(query="SELECT * FROM users")