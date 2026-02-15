from flask import Blueprint, render_template, request, jsonify
import hashlib

hash_generator_bp = Blueprint('hash_generator', __name__)

@hash_generator_bp.route('/')
def index():
    return render_template('tools/hash_generator.html')

@hash_generator_bp.route('/generate', methods=['POST'])
def generate():
    try:
        algorithm = request.form.get('algorithm')
        text = request.form.get('text')  # New HTML sends 'text'
        file = request.files.get('file') # New HTML sends 'file'

        if not algorithm:
            return jsonify({'status': 'error', 'message': 'Missing algorithm'})

        data_bytes = b""

        # Handle File vs Text
        if file:
            data_bytes = file.read()
        elif text:
            data_bytes = text.encode('utf-8')
        else:
            return jsonify({'status': 'error', 'message': 'No input provided (Text or File)'})

        # Generate Hash
        hash_obj = None
        if algorithm == 'sha256':
            hash_obj = hashlib.sha256(data_bytes)
        elif algorithm == 'sha512':
            hash_obj = hashlib.sha512(data_bytes)
        elif algorithm == 'md5':
            hash_obj = hashlib.md5(data_bytes)
        else:
            return jsonify({'status': 'error', 'message': 'Invalid algorithm'})

        return jsonify({'status': 'success', 'hash': hash_obj.hexdigest()})

    except Exception as e:
        print(f"Error in hash generator: {e}")
        return jsonify({'status': 'error', 'message': str(e)})