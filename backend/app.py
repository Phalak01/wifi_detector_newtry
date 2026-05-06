# backend/app.py

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import sqlite3
import os

app = Flask(__name__)

# ── Config ────────────────────────────────────────────────────────
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY",
    "wifi-threat-secret-2024-change-in-prod"
)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

# ── CORS: allow deployed frontend also ────────────────────────────
CORS(app)

jwt = JWTManager(app)

# ── Register route blueprints ─────────────────────────────────────
from routes.auth import auth_bp
from routes.wifi import wifi_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(wifi_bp, url_prefix="/wifi")

# ── Create SQLite DB + tables ─────────────────────────────────────
def init_db():
    db = os.path.join(os.path.dirname(__file__), "database.db")
    conn = sqlite3.connect(db)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("✓ Database ready (database.db)")

@app.route("/")
def home():
    return {"message": "WiFi Threat Analyzer API is live"}

@app.route("/status")
def status():
    return {"status": "online", "message": "WiFi Threat Analyzer backend running"}

# IMPORTANT: this runs on Render/Gunicorn too
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    print("\n" + "=" * 52)
    print("  WiFi Threat Analyzer — Backend API")
    print(f"  URL : http://localhost:{port}")
    print("  Docs: GET /status to verify")
    print("=" * 52 + "\n")

    app.run(host="0.0.0.0", port=port)