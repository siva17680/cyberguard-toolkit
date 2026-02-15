from flask import Blueprint, render_template, request, jsonify
import hashlib
import time

password_cracker_bp = Blueprint('password_cracker', __name__)

# Small dictionary for demo purposes
WORDLIST = ['123456', 'password', 'admin', 'welcome', '12345678', 'root', 'toor', 'qwerty']

@password_cracker_bp.route('/')
def index():
    return render_template('tools/password_cracker.html')

@password_cracker_bp.route('/crack', methods=['POST'])
def crack():
    target_hash = request.json.get('hash').strip().lower()
    algo = request.json.get('algo', 'md5')
    
    start_time = time.time()
    cracked_password = None
    
    # Real-world tools would iterate a massive file here
    for word in WORDLIST:
        if algo == 'md5':
            h = hashlib.md5(word.encode()).hexdigest()
        elif algo == 'sha256':
            h = hashlib.sha256(word.encode()).hexdigest()
            
        if h == target_hash:
            cracked_password = word
            break
            
    duration = round(time.time() - start_time, 4)
    
    if cracked_password:
        return jsonify({'status': 'success', 'password': cracked_password, 'time': duration})
    else:
        return jsonify({'status': 'fail', 'time': duration})