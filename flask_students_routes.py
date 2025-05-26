# Manages all the business logic for routes and data handling
from flask import jsonify, request
from redis_cache import redis_client
import json
from db import db, Student
import time
from sqlalchemy import inspect

# def check_postgres():
#     """Check if PostgreSQL is reachable and the 'student' table exists."""
#     try:
#         inspector = inspect(db.engine)
#         return inspector.has_table('student')  # More efficient check
#     except Exception as e:
#         print(f"Database connection error: {e}")
#         return False

def get_students():
    # Check PostgreSQL availability
    # if not check_postgres():
    #     return jsonify({"error": "PostgreSQL is down. Stopping execution."}), 500
    
    try:
        # Try to get data from Redis first
        cached_data = redis_client.get('students_all')
        if cached_data:
            return jsonify(json.loads(cached_data))

        else:
            print("student is not in redis yet")
            # If not in Redis, fetch from PostgreSQL
            students = Student.query.all()
            result = [{
                'id': student.id,
                'firstname': student.firstname,
                'lastname': student.lastname,
                'email': student.email,
                'age': student.age,
                'created_at': student.created_at.isoformat(),
                'bio': student.bio
            } for student in students]

            # Storing data in Redis - Cache the result for 1 hour
            redis_client.set('students_all', json.dumps(result), ex=3600)
            print("student is added to redis caching")
            return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Error accessing Redis: {str(e)}"}), 500
    

def get_student(id):
    # Ensure the id is treated as an integer
    try:
        id = int(id)  # Convert to integer if needed
    except ValueError:
        return jsonify({"error": "Invalid student ID"}), 400

    try:
        # Try to get data from Redis first
        cached_data = redis_client.get(f'student_{id}')
    except Exception as e:
        return jsonify({"error": f"Error accessing Redis: {str(e)}"}), 500
    
    if cached_data:
        # Serve data from cache (deserialized)
        return jsonify(json.loads(cached_data)) # json.loads Convert a JSON string into a Python object
    print("student is not in redis yet")
    
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    result = ({
        'id': student.id,
        'firstname': student.firstname,
        'lastname': student.lastname,
        'email': student.email,
        'age': student.age,
        'created_at': student.created_at.isoformat(),
        'bio': student.bio
    })
        # Cache the result for 1 hour
    redis_client.set(f'student_{id}', json.dumps(result), ex=3600) # json.dumps converts a Python object into a string
    print("student is added to redis caching")

    return jsonify(result)

def add_student():
    data = request.json
    try:
        # Create a new student object
        new_student = Student(
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            age=data['age'],
            bio=data['bio']
        )
        # Add to the database
        db.session.add(new_student)
        db.session.commit()

        # Invalidate the cache since the student list has changed
        redis_client.delete(f'student_{new_student.id}')        
        return jsonify({"message": "Student added successfully"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
