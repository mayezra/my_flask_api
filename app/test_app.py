from app import app  

# test for GET /students
def test_students_list():
    client = app.test_client()
    response = client.get('/students')
    assert response.status_code == 200

# test for GET /students/1
def test_single_student():
    client = app.test_client()
    response = client.get('/students/1')
    assert response.status_code == 200