from flask import Flask, jsonify
from flask_cors import CORS
from prometheus_client import generate_latest, Counter

app = Flask(__name__)
CORS(app)


REQUESTS = Counter('my_app_requests_total', 'Total number of requests')


@app.route('/api')
def api_message():
    REQUESTS.inc()  # Count API access
    return jsonify({'message': 'Hello from the Backend!'})


@app.route("/")
def home():
    return "Backend is running!"


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
