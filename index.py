import os
import sys
import json
import requests
from flask import Flask, render_template, request, jsonify


app = Flask(__name__, template_folder="templates")


def call_openrouter(message: str):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    payload = {
        "model": "openrouter/owl-alpha",
        "messages": [{"role": "user", "content": message}],
    }

    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    message = data.get("message", "Hello")
    try:
        result = call_openrouter(message)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Extract assistant content if available
    try:
        content = result["choices"][0]["message"]["content"]
    except Exception:
        content = None

    return jsonify({"raw": result, "text": content})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
