from flask import Flask, jsonify, request
import requests
import random
import threading
import time
import os
from hashing.consistent_hash import ConsistentHash

SERVER_PORTS = {
    1: 5000,
    2: 5002,
    3: 5003
}

app = Flask(__name__)

def spawn_server(server_id, hostname=None):

    if hostname is None:
        hostname = f"server{server_id}"

    host_port = SERVER_PORTS.get(server_id, 5000 + server_id)

    # Remove old container if it exists
    os.system(f"docker rm -f {hostname} >/dev/null 2>&1")

    command = (
        f"docker run -d "
        f"-p {host_port}:5000 "
        f"-e SERVER_ID={server_id} "
        f"--name {hostname} "
        f"distributed-server"
    )

    result = os.system(command)

    if result != 0:
        print(f"Failed to spawn {hostname}")
        return

    replicas[server_id] = {
        "hostname": hostname,
        "address": f"http://localhost:{host_port}"
    }

    hash_ring.add_server(server_id)

    print(f"Spawned {hostname}")

# Create the hash ring
hash_ring = ConsistentHash()

# Store replica information
replicas = {
    1: {
        "hostname": "server1",
        "address": f"http://localhost:{SERVER_PORTS[1]}"
    },
    2: {
        "hostname": "server2",
        "address": f"http://localhost:{SERVER_PORTS[2]}"
    },
    3: {
        "hostname": "server3",
        "address": f"http://localhost:{SERVER_PORTS[3]}"
    }
}

def monitor_servers():

    while True:

        failed_servers = []

        for server_id, server in list(replicas.items()):

            try:
                response = requests.get(
                    f"{server['address']}/heartbeat",
                    timeout=2
                )

                if response.status_code != 200:
                    failed_servers.append(server_id)

            except requests.exceptions.RequestException:
                failed_servers.append(server_id)

        for server_id in failed_servers:

            print(f"Server {server_id} has failed.")

            if server_id in replicas:

                hostname = replicas[server_id]["hostname"]

                # Remove from hash ring
                hash_ring.remove_server(server_id)

                # Remove docker container
                os.system(f"docker rm -f {hostname}")

                # Remove replica record
                del replicas[server_id]

            # Spawn replacement server
            spawn_server(server_id)

        time.sleep(5)

# Add the servers to the hash ring
for server_id in replicas:
    hash_ring.add_server(server_id)


@app.route("/rep", methods=["GET"])
def get_replicas():
    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": [server["hostname"] for server in replicas.values()]
        },
        "status": "successful"
    }), 200

@app.route("/add", methods=["POST"])
def add_servers():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Invalid JSON payload",
            "status": "failure"
        }), 400

    n = data.get("n")
    hostnames = data.get("hostnames", [])

    if n is None or n <= 0:
        return jsonify({
            "message": "Number of servers must be greater than zero",
            "status": "failure"
        }), 400

    if len(hostnames) > n:
        return jsonify({
            "message": "Length of hostname list is more than newly added instances",
            "status": "failure"
        }), 400

    next_id = max(replicas.keys()) + 1 if replicas else 1

    # Add servers with supplied hostnames
    for hostname in hostnames:
        spawn_server(next_id, hostname)
        next_id += 1

    # Generate remaining servers
    remaining = n - len(hostnames)

    for _ in range(remaining):
        spawn_server(next_id)
        next_id += 1

    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": [server["hostname"] for server in replicas.values()]
        },
        "status": "successful"
    }), 200

@app.route("/rm", methods=["DELETE"])
def remove_servers():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Invalid JSON payload",
            "status": "failure"
        }), 400

    n = data.get("n")
    hostnames = data.get("hostnames", [])

    if n is None or n <= 0:
        return jsonify({
            "message": "Number of servers must be greater than zero",
            "status": "failure"
        }), 400

    if len(hostnames) > n:
        return jsonify({
            "message": "Length of hostname list is more than removable instances",
            "status": "failure"
        }), 400

    removed = 0

    # Remove requested servers
    for hostname in hostnames:

        server_id = None

        for sid, server in replicas.items():
            if server["hostname"] == hostname:
                server_id = sid
                break

        if server_id is not None:
            hash_ring.remove_server(server_id)
            hostname = replicas[server_id]["hostname"]
            os.system(f"docker rm -f {hostname}")
            del replicas[server_id]
            removed += 1

    # Remove additional servers randomly
    while removed < n and replicas:

        server_id = random.choice(list(replicas.keys()))
        hostname = replicas[server_id]["hostname"]

        hash_ring.remove_server(server_id)

        os.system(f"docker rm -f {hostname}")

        del replicas[server_id]

        removed += 1

    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": [server["hostname"] for server in replicas.values()]
        },
        "status": "successful"
    }), 200


@app.route("/<path:path>", methods=["GET"])
def route_request(path):

    request_id = random.randint(100000, 999999)

    server_id = hash_ring.get_server(request_id)

    if server_id is None:
        return jsonify({
            "message": "No servers available",
            "status": "failure"
        }), 500

    address = replicas[server_id]["address"]

    try:

        response = requests.get(f"{address}/{path}")

        try:
            return jsonify(response.json()), response.status_code

        except ValueError:
            return jsonify({
                "message": f"Endpoint '/{path}' does not exist in server replicas",
                "status": "failure"
            }), 400

    except requests.exceptions.RequestException:

        return jsonify({
            "message": "Server unavailable",
            "status": "failure"
        }), 500

if __name__ == "__main__":

    os.system("docker rm -f server1 server2 server3 >/dev/null 2>&1")

    heartbeat_thread = threading.Thread(
        target=monitor_servers,
        daemon=True
    )
    heartbeat_thread.start()

    app.run(host="0.0.0.0", port=5001)
