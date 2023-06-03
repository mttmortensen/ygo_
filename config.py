import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

def get_db_config():
    db_config = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
    }
    return db_config
