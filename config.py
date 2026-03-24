import os
from dotenv import load_dotenv

load_dotenv()

SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY", "changeme")
PORT = int(os.getenv("PORT", 8888))
CLIENT_TIMEOUT = 60
