import os
from dotenv import load_dotenv

load_dotenv()

TTL = 3600

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")
BUCKET_NAME = os.getenv("BUCKET_NAME")

STORAGE_ADDRESS = 'https://df8bf80b-2458-4fcf-a60f-02849e8f8c70.selstorage.ru'
