from flask import Blueprint, render_template, request, jsonify
import re
import socket
from urllib.parse import urlparse

phishing_detector_bp = Blueprint('phishing_detector', __name__)

@phishing_detector_bp.route('/')
def index():
    return render_template('tools/phishing_detector.html')

@phishing_detector_bp.route('/analyze', methods=['POST'])
def analyze():
    url = request.json.get('url', '')
    parsed = urlparse(url)
    risk_score = 0
    flags = []

    # Check 1: Length
    if len(url) > 75:
        risk_score += 1
        flags.append("URL is suspiciously long.")

    # Check 2: IP Address instead of Domain
    domain = parsed.netloc
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain):
        risk_score += 3
        flags.append("Uses raw IP address instead of domain name.")

    # Check 3: Suspicious Keywords
    suspicious = ['login', 'verify', 'update', 'bank', 'secure', 'account', 'paypal']
    if any(s in url.lower() for s in suspicious):
        risk_score += 1
        flags.append("Contains sensitive keywords (login, bank, etc).")

    # Check 4: @ Symbol (Obfuscation)
    if "@" in url:
        risk_score += 2
        flags.append("Contains '@' symbol (Browser redirection trick).")

    # Classification
    if risk_score == 0:
        verdict = "Safe"
        color = "success"
    elif risk_score < 3:
        verdict = "Suspicious"
        color = "warning"
    else:
        verdict = "High Risk"
        color = "danger"

    return jsonify({
        'verdict': verdict,
        'color': color,
        'flags': flags
    })