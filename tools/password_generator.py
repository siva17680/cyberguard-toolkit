from flask import Blueprint, render_template, request, jsonify
import secrets
import string

password_generator_bp = Blueprint('password_generator', __name__)

@password_generator_bp.route('/')
def index():
    return render_template('tools/password_generator.html')

@password_generator_bp.route('/generate', methods=['POST'])
def generate():
    data = request.json
    length = int(data.get('length', 12))
    use_upper = data.get('upper', True)
    use_lower = data.get('lower', True)
    use_digits = data.get('digits', True)
    use_symbols = data.get('symbols', True)

    if length < 8: length = 8
    if length > 64: length = 64

    chars = ''
    if use_lower: chars += string.ascii_lowercase
    if use_upper: chars += string.ascii_uppercase
    if use_digits: chars += string.digits
    if use_symbols: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if not chars:
        return jsonify({'error': 'Select at least one character type'}), 400

    # Cryptographically secure generation
    password = ''.join(secrets.choice(chars) for _ in range(length))
    
    return jsonify({'password': password})