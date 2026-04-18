import os
from dotenv import load_dotenv
import logging 


load_dotenv()

TTL = 3600
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")
BUCKET_NAME = os.getenv("BUCKET_NAME")


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

STORAGE_ADDRESS = 'https://df8bf80b-2458-4fcf-a60f-02849e8f8c70.selstorage.ru'
DATABASE_URL = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'


logging.info(DATABASE_URL)
