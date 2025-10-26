import time

from flask import Flask, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)

# -------------------------
# Prometheus Metrics
# -------------------------
REQUEST_COUNT = Counter(
    "flask_request_count",
    "Total number of requests",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "flask_request_latency_seconds", "Request latency (seconds)", ["endpoint"]
)


@app.before_request
def start_timer():
    request.start_time = time.time()


@app.after_request
def record_request_data(response):
    if hasattr(request, "start_time"):
        latency = time.time() - request.start_time
        REQUEST_LATENCY.labels(request.path).observe(latency)
        REQUEST_COUNT.labels(
            request.method,
            request.path,
            response.status_code,
        ).inc()
    return response


@app.route("/health")
def health():
    return jsonify(status="healthy")


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
