from flask import jsonify, request
import json
from db import db, Student
from redis_cache import create_redis_client

# Get all students (Redis-cached)
def get_students():
    try:
        redis = create_redis_client()
        cached_data = None

        if redis:
            cached_data = redis.get("students_all")
            if cached_data:
                return jsonify(json.loads(cached_data))
        else:
            print("Redis is not available – fallback to DB")

        print("student is not in redis yet")
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

        if redis:
            redis.set("students_all", json.dumps(result), ex=3600)
            print("student data added to Redis cache")

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Error accessing students: {str(e)}"}), 500

# Get a student by ID (Redis-cached)
def get_student(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({"error": "Invalid student ID"}), 400

    try:
        redis = create_redis_client()
        cached_data = None

        if redis:
            cached_data = redis.get(f'student_{id}')
            if cached_data:
                return jsonify(json.loads(cached_data))
        else:
            print("Redis is not available – fallback to DB")

    except Exception as e:
        return jsonify({"error": f"Error accessing Redis: {str(e)}"}), 500

    print("student is not in redis yet")
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    result = {
        'id': student.id,
        'firstname': student.firstname,
        'lastname': student.lastname,
        'email': student.email,
        'age': student.age,
        'created_at': student.created_at.isoformat(),
        'bio': student.bio
    }

    if redis:
        redis.set(f'student_{id}', json.dumps(result), ex=3600)
        print("student is added to Redis cache")

    return jsonify(result)

# Add new student
def add_student():
    data = request.json
    try:
        new_student = Student(
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            age=data['age'],
            bio=data['bio']
        )
        db.session.add(new_student)
        db.session.commit()

        redis = create_redis_client()
        if redis:
            redis.delete(f'student_{new_student.id}')
            redis.delete('students_all')  # optional: refresh list cache too

        return jsonify({"message": "Student added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
