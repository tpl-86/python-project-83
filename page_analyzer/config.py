import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_SSL_MODE = os.getenv('DATABASE_SSL_MODE', 'disable')
