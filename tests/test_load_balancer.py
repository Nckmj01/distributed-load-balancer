import pytest
from unittest.mock import patch
from load_balancer import app as lb


@pytest.fixture(autouse=True)
def reset_state():
    lb.replicas.clear()
    lb.hash_ring = lb.ConsistentHash()


def test_rep_endpoint():
    client = lb.app.test_client()

    response = client.get("/rep")

    assert response.status_code == 200


@patch("load_balancer.app.spawn_server")
def test_add_servers(mock_spawn):
    client = lb.app.test_client()

    response = client.post(
        "/add",
        json={
            "n": 2
        }
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "successful"
    assert mock_spawn.call_count == 2
