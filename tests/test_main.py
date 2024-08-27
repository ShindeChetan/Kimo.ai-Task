from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_courses():
    response = client.get("/api/courses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_course():
    course_id = "66ccce7ed873663847280561"
    response = client.get(f"/api/courses/{course_id}")
    assert response.status_code in [200, 404]

def test_rate_chapter():
    course_id = "66ccce7ed873663847280561"
    chapter_name = "Introduction to Convolutional Neural Networks for Visual Recognition"
    response = client.post(f"/api/courses/{course_id}/chapters/{chapter_name}/rate", params="positive")
    assert response.status_code in [200, 404]
