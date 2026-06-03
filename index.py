import argparse
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


def start_ngrok(port: int):
    try:
        from pyngrok import ngrok
    except ModuleNotFoundError:
        print("pyngrok is not installed. Install with: pip install pyngrok", file=sys.stderr)
        return None

    auth_token = os.environ.get("NGROK_AUTHTOKEN")
    if auth_token:
        ngrok.set_auth_token(auth_token)

    try:
        tunnel = ngrok.connect(port, bind_tls=True)
        public_url = tunnel.public_url
        print(f"ngrok tunnel started: {public_url}")
        return public_url
    except Exception as e:
        print(f"Failed to start ngrok tunnel: {e}", file=sys.stderr)
        return None


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
    parser = argparse.ArgumentParser(description="Run Flask app with optional ngrok tunnel.")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 5000)), help="Port to run the Flask app on")
    parser.add_argument("--ngrok", action="store_true", help="Start an ngrok tunnel and print the public URL")
    args = parser.parse_args()

    if args.ngrok:
        start_ngrok(args.port)

    app.run(host="0.0.0.0", port=args.port, debug=True)
