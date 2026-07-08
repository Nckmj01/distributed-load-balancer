from hashing.consistent_hash import ConsistentHash


def test_add_servers():

    ring = ConsistentHash()

    ring.add_server(1)
    ring.add_server(2)
    ring.add_server(3)

    assert len(ring.servers) == 3


def test_request_mapping():

    ring = ConsistentHash()

    ring.add_server(1)
    ring.add_server(2)
    ring.add_server(3)

    server = ring.get_server(123456)

    assert server in [1, 2, 3]


def test_remove_server():

    ring = ConsistentHash()

    ring.add_server(1)
    ring.add_server(2)

    ring.remove_server(1)

    assert 1 not in ring.servers


def test_duplicate_server():

    ring = ConsistentHash()

    ring.add_server(1)
    ring.add_server(1)

    assert len(ring.servers) == 1
