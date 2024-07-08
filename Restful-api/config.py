# config.py

from dotenv import load_dotenv
import os

# Load environment variables from .env.config file
load_dotenv('.env.config')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
