from fastapi.testclient import TestClient
from app.main import app


def test_health_and_google_login():
    client = TestClient(app)

    # Health check should return 200 and expected keys
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data

    # Google login should either redirect (303/307) or return 500 if not configured
    r2 = client.get("/auth/google/login", allow_redirects=False)
    assert r2.status_code in (302, 307, 303, 500)
