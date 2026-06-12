import argparse
import os
import sys
import json
import requests
from flask import Flask, render_template, request, jsonify
from config import SQLALCHEMY_DATABASE_URI
from models import db, Report


app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app)


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


# Report CRUD Routes
@app.route("/api/reports", methods=["GET"])
def get_reports():
    """Get all reports."""
    try:
        reports = Report.query.all()
        return jsonify([report.to_dict() for report in reports])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/reports/<int:report_id>", methods=["GET"])
def get_report(report_id):
    """Get a specific report."""
    try:
        report = Report.query.get(report_id)
        if not report:
            return jsonify({"error": "Report not found"}), 404
        return jsonify(report.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/reports", methods=["POST"])
def create_report():
    """Create a new report."""
    try:
        data = request.get_json() or {}
        title = data.get("title", "Untitled Report")
        content = data.get("content", "")
        
        # Generate AI response if content is provided
        ai_response = None
        if content:
            try:
                ai_result = call_openrouter(content)
                ai_response = ai_result["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"Warning: Failed to get AI response: {e}")
        
        report = Report(title=title, content=content, ai_response=ai_response)
        db.session.add(report)
        db.session.commit()
        
        return jsonify(report.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/reports/<int:report_id>", methods=["PUT"])
def update_report(report_id):
    """Update an existing report."""
    try:
        report = Report.query.get(report_id)
        if not report:
            return jsonify({"error": "Report not found"}), 404
        
        data = request.get_json() or {}
        if "title" in data:
            report.title = data["title"]
        if "content" in data:
            report.content = data["content"]
        if "ai_response" in data:
            report.ai_response = data["ai_response"]
        
        db.session.commit()
        return jsonify(report.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/reports/<int:report_id>", methods=["DELETE"])
def delete_report(report_id):
    """Delete a report."""
    try:
        report = Report.query.get(report_id)
        if not report:
            return jsonify({"error": "Report not found"}), 404
        
        db.session.delete(report)
        db.session.commit()
        
        return jsonify({"message": "Report deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Flask app with optional ngrok tunnel.")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 5000)), help="Port to run the Flask app on")
    parser.add_argument("--ngrok", action="store_true", help="Start an ngrok tunnel and print the public URL")
    args = parser.parse_args()

    if args.ngrok:
        start_ngrok(args.port)

    app.run(host="0.0.0.0", port=args.port, debug=True)
