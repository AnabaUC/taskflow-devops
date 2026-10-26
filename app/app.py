from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Simple in-memory task storage
tasks = [
    {
        "id": 1,
        "title": "Learn Docker",
        "completed": False
    },
    {
        "id": 2,
        "title": "Learn Kubernetes",
        "completed": False
    }
]

# Prometheus metric
REQUEST_COUNT = Counter(
    "taskflow_requests_total",
    "Total number of requests received"
)


@app.before_request
def count_request():
    REQUEST_COUNT.inc()


@app.route("/")
def home():
    return jsonify({
        "application": "TaskFlow",
        "message": "TaskFlow API is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "completed": False
    }

    tasks.append(new_task)

    return jsonify(new_task), 201


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)