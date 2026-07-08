from server.app import app


def test_home_endpoint():
    client = app.test_client()

    response = client.get("/home")

    assert response.status_code == 200

    data = response.get_json()

    assert "message" in data
    assert "status" in data
    assert data["status"] == "successful"


def test_heartbeat_endpoint():
    client = app.test_client()

    response = client.get("/heartbeat")

    assert response.status_code == 200
