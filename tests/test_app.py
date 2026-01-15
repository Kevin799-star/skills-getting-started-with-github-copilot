from fastapi.testclient import TestClient
import pytest

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Make a shallow copy to restore after each test
    original = {k: {**v, "participants": list(v["participants"])} for k, v in activities.items()}
    yield
    activities.clear()
    activities.update(original)


def test_get_activities():
    client = TestClient(app)
    resp = client.get('/activities')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert 'Chess Club' in data


def test_signup_and_unregister():
    client = TestClient(app)
    activity = 'Chess Club'
    email = 'testuser@example.com'

    # Ensure not already present
    resp = client.get('/activities')
    assert email not in resp.json()[activity]['participants']

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]['participants']

    # Unregister
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert email not in activities[activity]['participants']
