import firebase_admin
from firebase_admin import credentials, auth, db
import os

# --------------------------------------------------------
# SIMPLE CONFIG (COMPATIBLE WITH OLD VERSIONS)
# --------------------------------------------------------
KEY_FILE = "serviceAccountKey.json"

if not os.path.exists(KEY_FILE):
    print(f"❌ [FIREBASE] CRITICAL: '{KEY_FILE}' not found!")

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(KEY_FILE)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://cyb3-9e1d3-default-rtdb.firebaseio.com/'
        })
        print("✅ [FIREBASE] Connected")
    except Exception as e:
        print(f"❌ [FIREBASE] Init Error: {e}")

def verify_token(id_token):
    print("   [AUTH] Verifying token...")
    try:
        # REMOVED clock_skew_seconds to prevent crashes on old versions
        decoded_token = auth.verify_id_token(id_token)
        print(f"   [AUTH] Success! User: {decoded_token.get('email')}")
        return decoded_token
    except Exception as e:
        # Print the EXACT error to the terminal so we can see it
        print(f"❌ [AUTH] Verification Failed: {type(e).__name__}: {e}")
        return None

def get_user_role(uid):
    try:
        ref = db.reference(f'users/{uid}')
        user_data = ref.get()
        return user_data.get('role', 'user') if user_data else 'user'
    except:
        return 'user'