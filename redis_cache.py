# Manages all the business logic for routes and data handling
from flask import Flask
import redis
# from flask_sqlalchemy import SQLAlchemy
from db import db

# Connect to Redis server (default settings)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Initialize SQLAlchemy
# db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 0
    # Initialize Flask and SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/students'  # PostgreSQL URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

    # Initialize extensions
    db.init_app(app)
    
    return app
