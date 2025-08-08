from flask import request, Response
from flask_students_routes import get_students, add_student, get_student  # Importing app, db, and Student from db.py
from redis_cache import create_app
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# test my workflow
app = create_app()

# Define a Prometheus metric: a counter that goes up for each request
REQUEST_COUNTER = Counter(
    "custom_requests_total",            # metric name (i will see this in Prometheus)
    "Total HTTP requests",              # description shown in /metrics
    ["method", "endpoint"]              # labels: used to filter & group in PromQL
)

# This runs before each request to your app
@app.before_request
def count_request():
    REQUEST_COUNTER.labels(
        method=request.method,          # Flask's built-in — it returns "GET", "POST", etc.
        endpoint=request.path           # from Flask — it gives you the URL path like "/" or "/students/2"
    ).inc()   

# First route (homepage)
@app.route('/')
def home():
    return "API is working!"

# A route that Prometheus will scrape metrics from
@app.route("/metrics")
def metrics():
    # generate_latest() collects and returns metrics in a format that Prometheus can scrape
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST) # This outputs all metrics (including our counter) in Prometheus format

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