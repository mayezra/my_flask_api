# Contains only the database model.
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


# app = create_app()
db = SQLAlchemy()

# Define Student model
class Student(db.Model):
    __tablename__ = 'student'  # The table name in the database (lowercase)
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'

