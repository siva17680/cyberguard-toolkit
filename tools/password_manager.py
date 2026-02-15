from flask import Blueprint, render_template, request, jsonify, session
from firebase_config import db
import uuid
import datetime

password_manager_bp = Blueprint('password_manager', __name__)

@password_manager_bp.route('/')
def index():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 403

    uid = session['user']['uid']
    
    # Fetch passwords from Firebase
    try:
        ref = db.reference(f'users/{uid}/passwords')
        passwords = ref.get() or {}
    except:
        passwords = {}

    return render_template('tools/password_manager.html', passwords=passwords)

@password_manager_bp.route('/add', methods=['POST'])
def add_password():
    if 'user' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    data = request.json
    uid = session['user']['uid']
    entry_id = str(uuid.uuid4())
    
    new_entry = {
        'service': data.get('service'),
        'username': data.get('username'),
        'password': data.get('password'), # Note: In a real app, encrypt this before saving!
        'created_at': str(datetime.datetime.now())
    }

    try:
        db.reference(f'users/{uid}/passwords/{entry_id}').set(new_entry)
        return jsonify({'status': 'success', 'message': 'Password saved successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@password_manager_bp.route('/delete/<entry_id>', methods=['POST'])
def delete_password(entry_id):
    if 'user' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    uid = session['user']['uid']
    try:
        db.reference(f'users/{uid}/passwords/{entry_id}').delete()
        return jsonify({'status': 'success', 'message': 'Entry deleted'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})