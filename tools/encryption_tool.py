import os
import base64
from flask import Blueprint, render_template, request, jsonify, send_file, after_this_request
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

encryption_tool_bp = Blueprint('encryption_tool', __name__)

def derive_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

@encryption_tool_bp.route('/')
def index():
    return render_template('tools/encryption_tool.html')

@encryption_tool_bp.route('/process', methods=['POST'])
def process():
    action = request.form.get('action') # encrypt or decrypt
    password = request.form.get('password')
    text = request.form.get('text')
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400

    try:
        if action == 'encrypt':
            salt = os.urandom(16)
            iv = os.urandom(12) # GCM standard IV size
            key = derive_key(password, salt)
            
            encryptor = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend()).encryptor()
            ciphertext = encryptor.update(text.encode()) + encryptor.finalize()
            
            # Pack: Salt(16) + IV(12) + Tag(16) + Ciphertext
            payload = salt + iv + encryptor.tag + ciphertext
            return jsonify({'result': base64.b64encode(payload).decode()})

        elif action == 'decrypt':
            data = base64.b64decode(text)
            salt, iv, tag = data[:16], data[16:28], data[28:44]
            ciphertext = data[44:]
            
            key = derive_key(password, salt)
            decryptor = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()).decryptor()
            decrypted = decryptor.update(ciphertext) + decryptor.finalize()
            
            return jsonify({'result': decrypted.decode()})
            
    except Exception as e:
        return jsonify({'error': 'Decryption failed. Wrong password or corrupted data.'}), 400