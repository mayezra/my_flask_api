# Manages all the business logic for routes and data handling
from flask import Flask
import redis
from db import db
from dotenv import load_dotenv
import os

# Load environment variables from the .env file (this will work with Docker Compose as well)
load_dotenv()

# Fetch environment variables from the .env file
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_HOST')  # default to 'localhost' if not set
db_name = os.getenv('POSTGRES_DB')  # default to 'students' if not set

# Connect to Redis server (default settings)
redis_client = redis.Redis(host='redis-db', port=6379, db=0)

# Initialize SQLAlchemy
# db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_HOST'] = 'redis-db'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 0
    # Initialize Flask and SQLAlchemy
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/students'  # PostgreSQL URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'  # PostgreSQL URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

    # Initialize extensions
    db.init_app(app)
    
    return app
