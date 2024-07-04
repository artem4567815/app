from dotenv import load_dotenv
import os

load_dotenv()

SERVER_ADDRESS = os.getenv('SERVER_ADDRESS')
SERVER_PORT = os.getenv('SERVER_PORT', 8080)
POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE', 'prod')
APP_DEBUG = bool(os.getenv('APP_DEBUG'))