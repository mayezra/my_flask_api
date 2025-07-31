from flask import jsonify, request, current_app
import json
from db import db, Student

def get_students():
    try:
        redis = current_app.redis_client  # safely get Redis
        cached_data = redis.get('students_all')
        if cached_data:
            return jsonify(json.loads(cached_data))

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

        redis.set('students_all', json.dumps(result), ex=3600)
        print("student is added to redis caching")
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Error accessing Redis: {str(e)}"}), 500

def get_student(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({"error": "Invalid student ID"}), 400

    try:
        redis = current_app.redis_client  
        cached_data = redis.get(f'student_{id}')
        if cached_data:
            return jsonify(json.loads(cached_data))
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

    redis.set(f'student_{id}', json.dumps(result), ex=3600)
    print("student is added to redis caching")

    return jsonify(result)

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

        redis = current_app.redis_client  
        redis.delete(f'student_{new_student.id}')

        return jsonify({"message": "Student added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
