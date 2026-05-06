# backend/routes/wifi.py
# Demo WiFi scanning + threat analysis

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime

wifi_bp = Blueprint("wifi", __name__)
scan_history = []


def _dbm_to_pct(dbm):
    return max(0, min(100, int((int(dbm) + 90) / 60 * 100)))


def score_network(ssid, encryption, signal_pct, hidden):
    pts = 0
    why = []
    fixes = []
    s = (ssid or "").lower()

    if encryption in ("OPEN", "None", "Open", ""):
        pts += 50
        why.append("No encryption — all traffic visible to anyone nearby")
        fixes.append("Never use for banking, email or passwords")
    elif encryption == "WEP":
        pts += 35
        why.append("WEP is obsolete and easily crackable")
        fixes.append("Avoid using WEP networks")
    elif encryption == "WPA":
        pts += 20
        why.append("WPA has known vulnerabilities")
        fixes.append("Prefer WPA2 or WPA3")
    elif encryption == "WPA2":
        pts += 5
        fixes.append("WPA2 is acceptable if AES is enabled")
    elif encryption == "WPA3":
        fixes.append("WPA3 is the current secure standard")
    else:
        pts += 10
        why.append(f"Unknown encryption type: {encryption}")

    bait = [
        "free", "public", "guest", "open", "hack", "test",
        "starbucks", "airport", "hotel", "cafe", "wifi", "hotspot",
        "linksys", "netgear", "tp-link", "dlink", "default"
    ]

    for w in bait:
        if w in s:
            pts += 20
            why.append(f"SSID contains '{w}' — common in fake WiFi networks")
            fixes.append("Verify this network before connecting")
            break

    if hidden:
        pts += 15
        why.append("Hidden SSID — unusual for normal public networks")
        fixes.append("Use caution with hidden networks")

    if signal_pct > 85 and encryption in ("OPEN", "None", ""):
        pts += 15
        why.append("Very strong open network signal — possible Evil Twin pattern")
        fixes.append("Avoid connecting to this network")

    if encryption in ("OPEN", "None", "") and any(w in s for w in bait):
        pts += 10
        why.append("Open network with suspicious name increases risk")

    pts = min(pts, 100)

    if pts >= 76:
        status, msg = "CRITICAL", "Extremely dangerous — do not connect"
    elif pts >= 51:
        status, msg = "HIGH", "High risk — avoid sensitive activities"
    elif pts >= 26:
        status, msg = "MEDIUM", "Moderate risk — use with caution"
    else:
        status, msg = "SAFE", "Appears safe — standard precautions apply"

    if not why:
        why.append("No major threat indicators detected")

    return {
        "score": pts,
        "status": status,
        "status_message": msg,
        "reasons": why,
        "recommendations": fixes
    }


def demo_scan():
    demo_networks = [
        {
            "id": 1,
            "ssid": "Home_WiFi",
            "encryption": "WPA2",
            "signal": -42,
            "signal_pct": 80,
            "channel": 6,
            "mac": "AA:11:22:33:44:55",
            "band": "2.4GHz",
            "hidden": False
        },
        {
            "id": 2,
            "ssid": "CoffeeShop_Free_WiFi",
            "encryption": "OPEN",
            "signal": -76,
            "signal_pct": 35,
            "channel": 11,
            "mac": "BB:11:22:33:44:55",
            "band": "2.4GHz",
            "hidden": False
        },
        {
            "id": 3,
            "ssid": "Office_5G",
            "encryption": "WPA3",
            "signal": -51,
            "signal_pct": 65,
            "channel": 36,
            "mac": "CC:11:22:33:44:55",
            "band": "5GHz",
            "hidden": False
        },
        {
            "id": 4,
            "ssid": "Hidden_Network",
            "encryption": "WPA2",
            "signal": -67,
            "signal_pct": 45,
            "channel": 44,
            "mac": "DD:11:22:33:44:55",
            "band": "5GHz",
            "hidden": True
        }
    ]

    for net in demo_networks:
        analysis = score_network(
            net["ssid"],
            net["encryption"],
            net["signal_pct"],
            net["hidden"]
        )

        net.update({
            "threat": analysis["score"],
            "status": analysis["status"],
            "reasons": analysis["reasons"],
            "recommendations": analysis["recommendations"]
        })

    return demo_networks


@wifi_bp.route("/scan", methods=["GET"])
@jwt_required()
def scan():
    nets = demo_scan()

    scan_history.append({
        "timestamp": datetime.now().isoformat(),
        "count": len(nets),
        "networks": nets
    })

    if len(scan_history) > 20:
        scan_history.pop(0)

    return jsonify({
        "success": True,
        "mode": "demo",
        "message": "Demo scan data shown because deployed cloud apps cannot access local WiFi hardware.",
        "count": len(nets),
        "networks": nets,
        "scanned_at": datetime.now().isoformat()
    })


@wifi_bp.route("/analyze", methods=["POST"])
@jwt_required()
def analyze():
    d = request.get_json() or {}

    ssid = d.get("ssid", "")
    encryption = d.get("encryption", "UNKNOWN")
    signal = int(d.get("signal", -70))
    hidden = bool(d.get("hidden", False))
    signal_pct = _dbm_to_pct(signal)

    a = score_network(ssid, encryption, signal_pct, hidden)

    return jsonify({
        "success": True,
        "ssid": ssid,
        "encryption": encryption,
        "signal_dbm": signal,
        "signal_pct": signal_pct,
        "risk": a["score"],
        "status": a["status"],
        "status_message": a["status_message"],
        "reason": " | ".join(a["reasons"]),
        "reasons": a["reasons"],
        "recommendations": a["recommendations"],
        "analyzed_at": datetime.now().isoformat()
    })


@wifi_bp.route("/history", methods=["GET"])
@jwt_required()
def history():
    return jsonify({
        "success": True,
        "history": scan_history[-10:]
    })