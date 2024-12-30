
import sqlite3

# Database connection function
def get_db_connection(db_path='/mnt/data/medical_ai_bot.db'):
    try:
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row  # Enables fetching rows as dictionaries
        return connection
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

# Function to close the database connection
def close_db_connection(connection):
    if connection:
        connection.close()
