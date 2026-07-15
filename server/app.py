from flask import Flask, jsonify
import os

# Create the Flask application instance.
app = Flask(__name__)

# Retrieve the unique server identifier from an environment variable.
# This allows each Docker container to identify itself when responding
# to client requests. If no ID is provided, "Unknown" is used.
SERVER_ID = os.getenv("SERVER_ID", "Unknown")


@app.route("/home", methods=["GET"])
def home():
    """
    Handles client requests routed by the load balancer.

    Returns:
        JSON response containing the server identifier and
        a success status message.
    """
    return jsonify({
        "message": f"Hello from Server: {SERVER_ID}",
        "status": "successful"
    }), 200


@app.route("/heartbeat", methods=["GET"])
def heartbeat():
    """
    Health check endpoint.

    Used by the load balancer to verify that the server
    instance is alive and responsive. Returns HTTP 200
    with an empty response body.
    """
    return "", 200


if __name__ == "__main__":
    # Start the Flask development server.
    # The host is set to 0.0.0.0 so the application can be
    # accessed by other Docker containers on the network.
    app.run(host="0.0.0.0", port=5000)
