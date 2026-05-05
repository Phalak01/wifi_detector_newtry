# WiFi Detector
 — Complete Setup Guide

## Project Structure
```
wifi-analyzer-complete/
│
├── backend/                  ← Python Flask API
│   ├── app.py                ← START HERE to run backend
│   ├── models.py             ← Database functions
│   ├── requirements.txt      ← Python packages
│   ├── database.db           ← Auto-created on first run
│   ├── routes/
│   │   ├── auth.py           ← /auth/register, /auth/login, /auth/me
│   │   └── wifi.py           ← /wifi/scan, /wifi/analyze, /wifi/history
│   └── utils/
│       └── __init__.py
│
└── frontend/                 ← React + Vite app
    ├── index.html
    ├── package.json          ← npm packages list
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    └── src/
        ├── main.jsx          ← React entry point
        ├── App.jsx           ← Routes
        ├── index.css         ← Global styles + animations
        ├── context/
        │   └── AuthContext.jsx   ← Global auth state (login/logout/user)
        ├── services/
        │   └── api.js            ← All axios API calls in one place
        ├── components/
        │   ├── Sidebar.jsx       ← Left navigation
        │   └── Navbar.jsx        ← Top header bar
        └── pages/
            ├── Login.jsx         ← /login
            ├── Signup.jsx        ← /signup
            ├── Dashboard.jsx     ← /dashboard (protected)
            └── Analysis.jsx      ← /analysis (protected, real scan)
```

---

## HOW TO RUN — Step by Step

### TERMINAL 1 — Backend (Python Flask)

**Step 1: Install Python**
Download from https://python.org (version 3.9 or higher)
During install, CHECK the box "Add Python to PATH"

**Step 2: Open terminal in the backend folder**
In VS Code: File → Open Folder → select `wifi-analyzer-complete/backend`
Press Ctrl+` to open terminal

**Step 3: Install Python packages**
```
pip install flask flask-cors flask-jwt-extended bcrypt
```
Wait for all packages to install (takes 1-2 minutes)

**Step 4: Start the backend**
```
python app.py
```
You should see:
```
✓ Database ready (database.db)
==================================================
  WiFi Threat Analyzer — Backend API
  URL : http://localhost:5000
==================================================
```

---

### TERMINAL 2 — Frontend (React)

**Step 5: Open a NEW terminal in the frontend folder**
In VS Code: click the + button in terminal to open a new one
Then: File → Open Folder → `wifi-analyzer-complete/frontend`
OR just cd into it:
```
cd ../frontend
```

**Step 6: Install npm packages (first time only)**
```
npm install
```

**Step 7: Start the frontend**
```
npm run dev
```
You should see:
```
VITE v5.x.x  ready in 300ms
➜  Local:   http://localhost:5173/
```

**Step 8: Open browser**
Go to: http://localhost:5173

---

## USING THE APP

1. **Register**: Click "Register" → fill in name, email, password → submit
2. **Login**: Use the email and password you just created
3. **Dashboard**: Shows your scan history and stats
4. **Scan & Analyze**:
   - Click "INITIATE REAL SCAN"
   - Backend uses your WiFi adapter to scan real nearby networks
   - All real networks appear with signal, encryption, threat score
   - Click any network row → get detailed AI threat analysis

---

## REAL WIFI SCANNING — OS Notes

### Windows
- Uses `netsh wlan show networks mode=bssid`
- **IMPORTANT**: Run VS Code or your terminal as **Administrator** for best results
  - Right-click VS Code → "Run as administrator"
- WiFi must be ON

### Mac
- Uses Apple's built-in airport utility
- WiFi must be ON
- May need to allow Terminal in System Preferences → Privacy → Full Disk Access

### Linux
- Uses `nmcli` (NetworkManager)
- If not installed: `sudo apt install network-manager`
- WiFi must be ON

---

## API Endpoints

| Method | URL | What it does | Auth needed? |
|--------|-----|-------------|--------------|
| POST | /auth/register | Create account | No |
| POST | /auth/login | Login, get JWT token | No |
| GET  | /auth/me | Get current user info | Yes (JWT) |
| GET  | /wifi/scan | Scan real nearby WiFi networks | Yes (JWT) |
| POST | /wifi/analyze | Analyze one network threat | Yes (JWT) |
| GET  | /wifi/history | Last 10 scan sessions | Yes (JWT) |
| GET  | /status | Check if backend is running | No |

---

## Common Errors

| Error | Fix |
|-------|-----|
| "Login failed — is the backend running?" | Start backend: `python app.py` in backend folder |
| "No networks found" on Windows | Run VS Code/terminal as Administrator |
| "pip not found" | Reinstall Python, check "Add to PATH" during install |
| "npm not found" | Install Node.js from nodejs.org |
| Port 5000 already in use | `python app.py` already running — check other terminals |
| Port 5173 already in use | `npm run dev -- --port 3000` |
| CORS error in browser | Make sure backend is running on port 5000 exactly |

---

## How Everything Connects

```
User fills Login form
        ↓
React calls POST /auth/login  (via api.js)
        ↓
Flask checks email + bcrypt password
        ↓
Returns JWT token
        ↓
Token stored in localStorage (key: wta_token)
        ↓
Every future API call auto-includes token (axios interceptor)
        ↓
User clicks INITIATE REAL SCAN
        ↓
React calls GET /wifi/scan  (with JWT)
        ↓
Flask runs netsh/airport/nmcli OS command
        ↓
Parses real nearby WiFi networks
        ↓
Calculates threat score for each network
        ↓
Returns JSON list of real networks
        ↓
React shows them in the UI
        ↓
User clicks a network row
        ↓
React calls POST /wifi/analyze  (with network data)
        ↓
Flask runs threat scoring engine
        ↓
Returns score, status, reasons, recommendations
        ↓
React shows full analysis panel
```
"# wifi_detector" 
