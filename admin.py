from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from firebase_admin import auth
from firebase_config import db
import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def dashboard():
    # Security Check: Only Admins Allowed
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        return redirect(url_for('login')) 
    
    # Fetch logs (last 50)
    logs_ref = db.reference('logs')
    logs_data = logs_ref.order_by_key().limit_to_last(50).get()
    
    formatted_logs = []
    if logs_data:
        # Firebase returns a dict; convert to list for easy sorting
        if isinstance(logs_data, dict):
            for key, val in logs_data.items():
                val['id'] = key
                formatted_logs.append(val)
        elif isinstance(logs_data, list):
             for log in logs_data:
                if log: formatted_logs.append(log)
        
        # Sort logs: Newest first
        formatted_logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

    # Fetch all users
    users_ref = db.reference('users')
    all_users = users_ref.get() or {}
    
    return render_template('admin_dashboard.html', logs=formatted_logs, users=all_users)

# --- CREATE USER ROUTE ---
@admin_bp.route('/create_user', methods=['POST'])
def create_user():
    if session.get('user')['role'] != 'admin': return jsonify({'error': 'Unauthorized'}), 403

    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role', 'user')

    if not email or not password:
         return jsonify({'status': 'error', 'message': 'Email and Password required'}), 400

    try:
        # 1. Create in Firebase Auth System
        user_record = auth.create_user(email=email, password=password)
        
        # 2. Add to Database with metadata
        uid = user_record.uid
        db.reference(f'users/{uid}').set({
            'email': email,
            'role': role,
            'active': True,  # Active by default
            'created_at': str(datetime.datetime.now())
        })
        
        return jsonify({'status': 'success', 'message': f'User {email} created successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# --- TOGGLE STATUS ROUTE (Activate/Deactivate) ---
@admin_bp.route('/toggle_status/<uid>', methods=['POST'])
def toggle_status(uid):
    if session.get('user')['role'] != 'admin': return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        ref = db.reference(f'users/{uid}')
        # Get current status, default to True if missing
        current_status = ref.child('active').get() 
        if current_status is None: current_status = True
        
        new_status = not current_status
        
        # Update DB
        ref.update({'active': new_status})
        
        # Update Firebase Auth (Locks/Unlocks the account)
        try:
            auth.update_user(uid, disabled=not new_status)
        except Exception as auth_error:
            print(f"Warning: Could not update Auth status: {auth_error}")
        
        return jsonify({'status': 'success', 'new_status': new_status})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# --- DELETE USER ROUTE ---
@admin_bp.route('/delete_user/<uid>', methods=['POST'])
def delete_user(uid):
    if session.get('user')['role'] != 'admin': return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Delete from Auth System
        try:
            auth.delete_user(uid)
        except:
            print(f"User {uid} already deleted from Auth or not found.")
        
        # Delete from Database
        db.reference(f'users/{uid}').delete()
        
        return jsonify({'status': 'success', 'message': 'User deleted'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})