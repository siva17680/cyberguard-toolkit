from flask import Blueprint, render_template, request, jsonify, stream_with_context, Response
import requests

directory_bruteforce_bp = Blueprint('directory_bruteforce', __name__)

COMMON_PATHS = ['admin', 'login', 'dashboard', 'config', 'backup', 'db', 'uploads', '.env', '.git']

@directory_bruteforce_bp.route('/')
def index():
    return render_template('tools/directory_bruteforce.html')

@directory_bruteforce_bp.route('/scan', methods=['POST'])
def scan():
    target = request.json.get('url')
    if not target.startswith('http'):
        target = 'http://' + target
    
    # Normally this would be a long running task. 
    # We will simulate a scan of limited paths for the web demo to avoid timeout.
    
    results = []
    
    for path in COMMON_PATHS:
        url = f"{target.rstrip('/')}/{path}"
        try:
            res = requests.head(url, timeout=2)
            if res.status_code != 404:
                results.append({
                    'path': f"/{path}",
                    'status': res.status_code,
                    'url': url
                })
        except:
            pass

    return jsonify({'results': results})