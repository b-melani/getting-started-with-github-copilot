import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "student1@mergington.edu"
    # Signup
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]
    # Duplicate signup
    dup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert dup_resp.status_code == 400
    # Unregister
    unreg_resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unreg_resp.status_code == 200
    assert f"Removed {email}" in unreg_resp.json()["message"]
    # Unregister again (should fail)
    unreg_fail = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unreg_fail.status_code == 404


def test_signup_invalid_activity():
    resp = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert resp.status_code == 404


def test_unregister_invalid_activity():
    resp = client.post("/activities/Nonexistent/unregister?email=ghost@mergington.edu")
    assert resp.status_code == 404
