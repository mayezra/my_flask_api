from flask_students_routes import get_students, add_student, get_student  # Importing app, db, and Student from db.py
from redis_cache import create_app


app = create_app()

# First route (homepage)
@app.route('/')
def home():
    return "API is working!"

# Add a new student
@app.route('/students', methods=['POST'])
def flask_add_student():
    return add_student()

# Get all students
@app.route('/students', methods=['GET'])
def flask_get_students():
    return get_students()

# Get a specific student by ID
@app.route('/students/<int:id>', methods=['GET'])
def flask_get_student(id):
    return get_student(id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
