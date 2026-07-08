import pytest
import requests
import time

BASE_URL = "http://localhost:5001"


def test_home_endpoint():
    response = requests.get(f"{BASE_URL}/home")

    assert response.status_code == 200

    data = response.json()

    assert "message" in data
    assert "Hello from Server:" in data["message"]


def test_rep_endpoint():
    response = requests.get(f"{BASE_URL}/rep")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "successful"
    assert "N" in data["message"]
    assert "replicas" in data["message"]


def test_add_endpoint():
    response = requests.post(
        f"{BASE_URL}/add",
        json={"n": 1}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "successful"

    # Give the new container time to start
    time.sleep(2)


def test_remove_endpoint():
    response = requests.delete(
        f"{BASE_URL}/rm",
        json={"n": 1}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "successful"


def test_invalid_endpoint():
    response = requests.get(f"{BASE_URL}/this_endpoint_does_not_exist")

    assert response.status_code in [400, 404]
