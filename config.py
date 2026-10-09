import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "student_management"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD","Mohamedaasif1"),
        port=os.getenv("DB_PORT", "5432")
    )