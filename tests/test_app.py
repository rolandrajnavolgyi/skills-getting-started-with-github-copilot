from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_duplicate_participant():
    activity_name = "Chess Club"
    email = "duplicate@example.com"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    duplicate_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert duplicate_response.status_code == 400


def test_unregister_participant_removes_email():
    activity_name = "Basketball Team"
    email = "remove@example.com"

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]
