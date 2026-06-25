import os # os.getenv 
from dotenv import load_dotenv # read .env file
import psycopg # PostgreSQL adapter 

load_dotenv() # Load .env file

DATABASE_URL = os.getenv("DATABASE_URL") 

def get_db_connection():
    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable is not set.")
    return psycopg.connect(DATABASE_URL)