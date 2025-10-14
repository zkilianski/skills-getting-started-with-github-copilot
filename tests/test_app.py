import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_signup_and_unregister():
    # Use a unique email for testing
    activity_name = list(client.get("/activities").json().keys())[0]
    test_email = "testuser@mergington.edu"

    # Ensure not already registered
    client.delete(f"/activities/{activity_name}/unregister?email={test_email}")

    # Sign up
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert response.status_code == 400

    # Unregister
    response = client.delete(f"/activities/{activity_name}/unregister?email={test_email}")
    assert response.status_code == 200
    assert f"Unregistered {test_email}" in response.json()["message"]

    # Unregister again should fail
    response = client.delete(f"/activities/{activity_name}/unregister?email={test_email}")
    assert response.status_code == 404
