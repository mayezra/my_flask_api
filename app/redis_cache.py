# Manages all the business logic for routes and data handling
from flask import Flask
import redis
from db import db
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
# load_dotenv()

# Fetch environment variables from the .env file
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_HOST')  # default to 'localhost' if not set
db_name = os.getenv('POSTGRES_DB')  # default to 'students' if not set


def create_redis_client():
    """Create and test Redis connection"""
    try:
        redis_host = os.getenv('CACHE_REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('CACHE_REDIS_PORT', 6379))
        redis_db = int(os.getenv('CACHE_REDIS_DB', 0))
        
        logger.info(f"Attempting to connect to Redis at {redis_host}:{redis_port}, db={redis_db}")
        
        # Create Redis client with additional configuration
        redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
        )
        
        # Test the connection
        redis_client.ping()
        logger.info("Successfully connected to Redis!")
        return redis_client
        
    except redis.ConnectionError as e:
        logger.error(f"Redis connection error: {e}")
        logger.error(f"Check if Redis is running at {redis_host}:{redis_port}")
        return None
    except redis.AuthenticationError as e:
        logger.error(f"Redis authentication error: {e}")
        logger.error("Check your Redis password configuration")
        return None
    except Exception as e:
        logger.error(f"Unexpected Redis error: {e}")
        return None

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'  # PostgreSQL URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

    # Initialize extensions
    db.init_app(app)
    
    # Connect to Redis server (default settings)
    redis_client = create_redis_client()
    if redis_client is None:
        logger.warning("Redis connection failed - running without cache")
        app.redis_client = None
    else:
        app.redis_client = redis_client
    return app
