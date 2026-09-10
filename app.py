"""student-ml-api: a minimal ML inference service used for the MLOps workflow exercise."""
from pathlib import Path

from flask import Flask, jsonify, request

APP_NAME = "student-ml-api"
VERSION_FILE = Path(__file__).resolve().parent / "VERSION"


def read_version() -> str:
    """Read the application version from the VERSION file (single source of truth)."""
    try:
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return "0.0.0"


APP_VERSION = read_version()

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": APP_NAME,
        "version": APP_VERSION,
    }), 200


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "value" not in data:
        return jsonify({"error": "Missing required field: 'value'"}), 400

    value = data["value"]
    # bool is a subclass of int in Python, so reject it explicitly
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return jsonify({"error": "Field 'value' must be a number"}), 400

    # Simple "model": the exercise is about the MLOps workflow, not ML accuracy
    prediction = value * 2
    return jsonify({"input": value, "prediction": prediction}), 200


if __name__ == "__main__":
    # 0.0.0.0 so the app is reachable from outside the container
    app.run(host="0.0.0.0", port=5000)
