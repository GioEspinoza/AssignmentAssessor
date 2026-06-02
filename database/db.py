import os # need access to os.getenv to read environment variables
from dotenv import load_dotenv # load_dotenv is used to read the .env file and set environment variables, including DATABASE_URL
import psycopg # psycopg is a PostgreSQL adapter for Python, used to connect to the database and execute SQL queries

load_dotenv() # Load environment variables from the .env file, making them available in the application. This allows us to keep sensitive information like database credentials out of the source code and instead read them from the environment.

DATABASE_URL = os.getenv("DATABASE_URL") # Retrieve the DATABASE_URL environment variable, which contains the connection string for the PostgreSQL database. This connection string includes the username, password, host, port, and database name needed to establish a connection to the database.

def get_db_connection(): # Define a function to establish and return a connection to the PostgreSQL database using the psycopg library. This function will be called whenever the application needs to interact with the database.
    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable is not set.")
    return psycopg.connect(DATABASE_URL) # Use the psycopg library to connect to the PostgreSQL database using the connection string provided in the DATABASE_URL environment variable. This function will return a connection object that can be used to execute SQL queries and interact with the database
