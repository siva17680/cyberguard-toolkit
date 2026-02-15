from flask import Blueprint, render_template, request, jsonify
import zxcvbn
import re

password_checker_bp = Blueprint('password_checker', __name__)

@password_checker_bp.route('/', methods=['GET'])
def index():
    return render_template('tools/password_checker.html')

@password_checker_bp.route('/analyze', methods=['POST'])
def analyze():
    password = request.json.get('password', '')
    
    if not password:
        return jsonify({'error': 'No password provided'}), 400

    # 1. zxcvbn Analysis (Entropy & Dictionary)
    results = zxcvbn.zxcvbn(password)
    score = results['score']  # 0-4
    crack_time = results['crack_times_display']['offline_slow_hashing_1e4_per_second']
    
    # 2. Custom Regex Analysis
    analysis = {
        'length': len(password),
        'has_upper': bool(re.search(r'[A-Z]', password)),
        'has_lower': bool(re.search(r'[a-z]', password)),
        'has_digit': bool(re.search(r'\d', password)),
        'has_special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
    }

    # 3. Strength Classification
    strength_map = {0: 'Very Weak', 1: 'Weak', 2: 'Medium', 3: 'Strong', 4: 'Very Strong'}
    
    return jsonify({
        'score': score,
        'strength': strength_map[score],
        'crack_time': crack_time,
        'feedback': results['feedback']['warning'],
        'details': analysis
    })