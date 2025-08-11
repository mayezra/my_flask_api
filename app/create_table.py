from redis_cache import create_app
from db import db, Student  # your model is here

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Student table created!")
