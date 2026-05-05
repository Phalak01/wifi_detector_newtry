# backend/app.py
import streamlit as st
import sqlite3, os

# ── UI ───────────────────────────────────────────────────────────
st.title("📶 WiFi Detector")
st.success("Backend is running 🚀")
st.write("This is your deployed Streamlit app")

# ── Database Setup (same logic preserved) ─────────────────────────
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

# Initialize DB
init_db()

# ── Status Logic (converted from Flask route) ─────────────────────
def get_status():
    return {
        "status": "online",
        "message": "WiFi Threat Analyzer backend running"
    }

# ── UI Interaction ───────────────────────────────────────────────
if st.button("Check Status"):
    result = get_status()
    st.json(result)

