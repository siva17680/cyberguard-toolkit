from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from firebase_config import verify_token, get_user_role, db
# Tool Blueprints
from tools.password_checker import password_checker_bp
from tools.password_generator import password_generator_bp
from tools.hash_generator import hash_generator_bp
from tools.encryption_tool import encryption_tool_bp
from tools.phishing_detector import phishing_detector_bp
from tools.steganography_tool import steganography_bp
from tools.metadata_checker import metadata_checker_bp
from tools.directory_bruteforce import directory_bruteforce_bp
from tools.password_cracker import password_cracker_bp
from tools.password_manager import password_manager_bp
from tools.browser_analyzer import browser_analyzer_bp
# Admin Blueprint
from admin import admin_bp
import os
import datetime
import psutil # <--- NEW IMPORT FOR RAM DETECTION

app = Flask(__name__)
app.config.from_object('config.Config')

# Register Blueprints
app.register_blueprint(password_checker_bp, url_prefix='/tools/password-checker')
app.register_blueprint(password_generator_bp, url_prefix='/tools/password-generator')
app.register_blueprint(hash_generator_bp, url_prefix='/tools/hash-generator')
app.register_blueprint(encryption_tool_bp, url_prefix='/tools/encryption')
app.register_blueprint(phishing_detector_bp, url_prefix='/tools/phishing-detector')
app.register_blueprint(steganography_bp, url_prefix='/tools/steganography')
app.register_blueprint(metadata_checker_bp, url_prefix='/tools/metadata-checker')
app.register_blueprint(directory_bruteforce_bp, url_prefix='/tools/directory-bruteforce')
app.register_blueprint(password_cracker_bp, url_prefix='/tools/password-cracker')
app.register_blueprint(password_manager_bp, url_prefix='/tools/password-manager')
app.register_blueprint(browser_analyzer_bp, url_prefix='/tools/browser-analyzer')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("\n📨 [LOGIN] Received POST request")
        
        try:
            # 1. Get Token
            data = request.json
            if not data:
                return jsonify({'status': 'error', 'message': 'No data received'}), 400
            
            id_token = data.get('idToken')
            if not id_token:
                return jsonify({'status': 'error', 'message': 'Missing ID Token'}), 400

            # 2. Verify Token
            decoded_token = verify_token(id_token)
            
            if decoded_token:
                uid = decoded_token['uid']
                email = decoded_token['email']
                
                # 3. Get Role from DB
                role = get_user_role(uid)
                print(f"   [LOGIN] User: {email} | Role: {role}")

                # 4. Save Session & Start Timer
                session['user'] = {'uid': uid, 'email': email, 'role': role}
                session['login_time'] = str(datetime.datetime.now()) # Track start time
                
                # 5. Log Login Activity
                try:
                    log_ref = db.reference('logs')
                    log_ref.push({
                        'uid': uid,
                        'email': email,
                        'action': 'login',
                        'timestamp': str(datetime.datetime.now())
                    })
                except Exception as e:
                    print(f"⚠️ [LOGS] Failed to save log: {e}")
                
                return jsonify({'status': 'success', 'redirect': url_for('dashboard')})
            
            else:
                print("⛔ [LOGIN] Token verification failed")
                return jsonify({'status': 'error', 'message': 'Invalid or Expired Token'}), 401

        except Exception as e:
            print(f"❌ [CRITICAL ERROR] Login Route Crashed: {e}")
            return jsonify({'status': 'error', 'message': f"Server Error: {str(e)}"}), 500
        
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # --- NEW: Get Real System RAM (Server Side) ---
    try:
        mem = psutil.virtual_memory()
        total_ram = round(mem.total / (1024 ** 3), 2)     # Convert Bytes to GB
        free_ram = round(mem.available / (1024 ** 3), 2)  # Convert Bytes to GB
    except Exception as e:
        print(f"Error reading RAM: {e}")
        total_ram = "N/A"
        free_ram = "N/A"

    return render_template('dashboard.html', 
                           user=session['user'], 
                           total_ram=total_ram, 
                           free_ram=free_ram)

@app.route('/logout')
def logout():
    if 'user' in session:
        uid = session['user']['uid']
        email = session['user']['email']
        
        # Calculate Session Duration
        duration_str = None
        login_time_str = session.get('login_time')
        
        if login_time_str:
            try:
                login_time = datetime.datetime.fromisoformat(login_time_str)
                logout_time = datetime.datetime.now()
                diff = logout_time - login_time
                duration_str = str(diff).split('.')[0] # Format H:M:S
            except Exception as e:
                print(f"Error calculating duration: {e}")

        # Save Logout Log with Duration
        try:
            log_ref = db.reference('logs')
            log_ref.push({
                'uid': uid,
                'email': email,
                'action': 'logout',
                'timestamp': str(datetime.datetime.now()),
                'duration': duration_str if duration_str else "N/A"
            })
        except:
            pass
            
    # Clear Session
    session.pop('user', None)
    session.pop('login_time', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, port=5000)