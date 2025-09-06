# backend/app.py  (replace contact route with this version)
import os
import html
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import re

app = Flask(__name__)
CORS(app)

# load env
load_dotenv()  # loads .env in development
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)


print("RESEND_API_KEY:", os.getenv("RESEND_API_KEY"))
print("RESEND_FROM:", os.getenv("RESEND_FROM"))
print("RESEND_TO:", os.getenv("RESEND_TO"))


def is_valid_email(value: str) -> bool:
    import re
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value))

PROJECTS = [
    {
        "id": 1,
        "title": "Little Lemon CLI",
        "tagline": "Restaurant reservations CLI with SQLAlchemy",
        "stack": ["Python", "SQLAlchemy", "Alembic", "Rich"],
        "image": "https://res.cloudinary.com/duskerco4/image/upload/v1757175477/little_lemon_mock-up_1_en3ciu.png",
        "links": {
            "github": "https://github.com/ms-njuguna/Little-Lemon-CLI",
            "live": ""
        },
        "summary": "A production-like CLI system for reservations with migrations, validators, and reports.",
        "highlights": [
            "Alembic migrations for schema evolution",
            "Rich TUI tables & prompts",
            "Robust validators for emails/phones"
        ]
    },
    {
        "id": 2,
        "title": "Verdara SPA",
        "tagline": "Single-page beauty/makeup shop using public API",
        "stack": ["HTML5", "Tailwind", "Javascript"],
        "image": "https://res.cloudinary.com/duskerco4/image/upload/v1757173514/verdara_image_pyjzf7.png",
        "links": {
            "github": "https://github.com/Ms-Njuguna/Verdara",
            "live": "https://ms-njuguna.github.io/Verdara/"
        },
        "summary": "SPA that fetches products, supports cart & first-time discounts.",
        "highlights": [
            "Debounced search & filters",
            "Optimistic UI for cart actions",
            "Graceful API error handling"
        ]
    },
    {
        "id": 3,
        "title": "HikeKenya App",
        "tagline": "CRUD app with JSON server",
        "stack": ["React + Vite", "JSON Server", "DOM"],
        "image": "https://res.cloudinary.com/duskerco4/image/upload/v1757175084/hikekenya_image_utqlc3.png",
        "links": {
                "github": "https://github.com/Ms-Njuguna/HikeKenya",
                "live": ""
        },
        "summary": "Learn-by-building app with ratings, comments, and filters.",
        "highlights": [
            "Modular DOM utilities",
            "Pagination & client-side caching",
            "Accessible keyboard navigation"
        ]
    }
]

def is_valid_email(value: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value))

@app.get("/api/hello")
def hello():
    return jsonify(message="Hello from Flask 👋")

@app.get("/api/projects")
def get_projects():
    return jsonify(projects=PROJECTS)

@app.post("/api/contact")
def contact():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify(success=False, error="Invalid JSON"), 400

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify(success=False, error="All fields are required."), 400
    if not is_valid_email(email):
        return jsonify(success=False, error="Invalid email format."), 400
    if len(message) > 5000:
        return jsonify(success=False, error="Message too long."), 400

    # sanitize user input for HTML
    safe_name = html.escape(name)
    safe_email = html.escape(email)
    safe_message = html.escape(message).replace("\n", "<br>")

    # compose HTML body
    html_body = f"""
      <h3>New portfolio message</h3>
      <p><strong>Name:</strong> {safe_name}</p>
      <p><strong>Email:</strong> {safe_email}</p>
      <hr/>
      <p><strong>Message:</strong></p>
      <p>{safe_message}</p>
    """

    from_addr = os.getenv("RESEND_FROM") or "Portfolio <onboarding@resend.dev>"
    to_addr = os.getenv("RESEND_TO")

    try:
        # Send via Resend Python SDK
        resp = resend.Emails.send({
            "from": from_addr,
            "to": [to_addr],
            "subject": f"Portfolio contact from {name}",
            "html": html_body,
            # include reply_to so you can reply to the sender quickly
            "reply_to": email
        })
        logging.info("Resend response: %s", resp)
    except Exception as exc:
        logging.exception("❌ Failed to send contact email: %s", exc)
        return jsonify(success=False, error=str(exc)), 500

    # Respond with confirmation and echo back the message (safe)
    return jsonify(success=True, received={"name": name, "email": email, "message": message}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
