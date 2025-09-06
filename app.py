from flask import Flask, jsonify, request
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

PROJECTS = [
    {
        "id": 1,
        "title": "Little Lemon CLI",
        "tagline": "Restaurant reservations CLI with SQLAlchemy",
        "stack": ["Python", "SQLAlchemy", "Alembic", "Rich"],
        "image": "https://picsum.photos/seed/lemon/800/500",
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
        "title": "Maybelline Makeup SPA",
        "tagline": "Single-page shop using public API",
        "stack": ["React", "Tailwind", "Fetch"],
        "image": "https://picsum.photos/seed/makeup/800/500",
        "links": {
            "github": "https://github.com/ms-njuguna/makeup-spa",
            "live": "https://makeup-spa.example.com"
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
        "title": "Beer Review App",
        "tagline": "CRUD app with JSON server",
        "stack": ["JS", "JSON Server", "DOM"],
        "image": "https://picsum.photos/seed/beer/800/500",
        "links": {
                "github": "https://github.com/ms-njuguna/beer-review",
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
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify(success=False, error="All fields are required."), 400
    if not is_valid_email(email):
        return jsonify(success=False, error="Invalid email format."), 400

    # TODO: save to DB or forward to email (Resend/SMTP)
    return jsonify(success=True, received={"name": name, "email": email})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
