# 🛡️ CyberGuard Toolkit – Advanced Cybersecurity Utility Suite

**CyberGuard Toolkit** is a powerful, web-based cybersecurity toolkit built with **Python (Flask)** and **Firebase**, designed for ethical security testing, encryption, analysis, and password management.

It provides a unified dashboard with 11+ essential cybersecurity tools wrapped in a high-contrast cyberpunk-inspired interface for an immersive user experience.

---

## 🔎 SEO Keywords

Cybersecurity Toolkit, Python Security Tools, Flask Cybersecurity Project, Encryption Toolkit, AES Encryption Tool, Password Strength Analyzer, Hash Generator, Ethical Hacking Toolkit, Firebase Security App, Web Security Scanner

---

## 🚀 Live Overview

CyberGuard Toolkit combines:

- 🔐 Encryption & Hashing Tools  
- 🧠 Password Analysis & Generation  
- 🌐 Web Security & Directory Scanning  
- 🗄️ Secure Firebase-backed Password Vault  
- 🖥️ Real-Time System Monitoring  
- 👨‍💻 Admin Management Console  

---

## 🧩 Tech Stack

| Technology | Purpose |
|------------|----------|
| **Python 3.10+** | Backend Programming |
| **Flask** | Web Framework |
| **Firebase** | Authentication & Database |
| **Bootstrap 5** | Responsive UI |
| **psutil** | System Monitoring |
| **Pillow** | Image Processing |
| **Requests** | API & HTTP Handling |

---

## ✨ Core Features

### 🖥️ Interactive Dashboard
- Cyberpunk-themed UI (Neon Green & Cyan accents)
- Optimized Matrix Binary Rain background animation
- Real-time Host RAM Monitoring using `psutil`
- Secure Admin Panel for user & log management

---

## 🛠️ Security Tools Included

1. **Password Strength Analyzer**  
   - Entropy calculation  
   - Estimated crack-time analysis  

2. **Secure Password Generator**  
   - Cryptographically secure passwords  

3. **Hash Generator**  
   - SHA-256  
   - SHA-512  
   - MD5  
   - File & Text hashing  

4. **AES-256-GCM Encryption Tool**  
   - Secure text & file encryption  
   - Authenticated decryption  

5. **Phishing URL Scanner**  
   - Heuristic-based suspicious link detection  

6. **Steganography Tool**  
   - LSB Encoding (Hide secret messages in images)  
   - Decode hidden messages  

7. **Metadata Extractor**  
   - Extract EXIF data from images  
   - View hidden metadata in PDFs  

8. **Directory Scanner**  
   - Ethical web directory brute-force testing  

9. **Hash Cracker (Educational)**  
   - Dictionary attack demonstration  

10. **Browser Fingerprinting Analyzer**  
   - Detect browser data leakage  

11. **Secure Password Manager**  
   - Firebase-backed encrypted credential vault  

---

# 📦 Installation Guide

## ✅ Prerequisites

- Python 3.10+
- Firebase Project (Google Cloud)

---

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/cyberguard-toolkit.git
cd cyberguard-toolkit
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, install:

```
flask
firebase-admin
psutil
Pillow
requests
cryptography
```

---

## 3️⃣ Firebase Setup

1. Go to **Firebase Console**
2. Create a project
3. Enable:
   - Email/Password Authentication
   - Realtime Database
4. Go to **Project Settings → Service Accounts**
5. Generate a new private key
6. Rename the file to:

```
serviceAccountKey.json
```

7. Place it in the project root

⚠️ **IMPORTANT:**  
Add this file to `.gitignore` to prevent committing credentials.

---

## 4️⃣ Run Application

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# 📂 Project Structure

```
cyberguard-toolkit/
│
├── app.py
├── admin.py
├── firebase_config.py
├── serviceAccountKey.json  (DO NOT COMMIT)
│
├── static/
│   ├── css/style.css
│   └── js/main.js
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── admin_dashboard.html
│   └── tools/
│
└── tools/
    ├── hash_generator.py
    ├── password_manager.py
    └── ...
```

---

# ⚠️ Ethical Use Disclaimer

CyberGuard Toolkit is developed strictly for:

- Educational purposes  
- Ethical security testing  
- Research & awareness  

❌ Do NOT use:

- Directory Scanner on unauthorized websites  
- Hash Cracker to compromise accounts  
- Phishing Scanner for malicious targeting  

The developers are not responsible for misuse.

---

# 🤝 Contributing

Contributions are welcome!

```bash
git checkout -b feature/YourFeature
git commit -m "Add YourFeature"
git push origin feature/YourFeature
```

Then open a Pull Request 🚀

---

# 👨‍💻 Authors

**Lead Developer:**  
Sivanujan Sivakumar  

**Co-Author:**  
Thishanth Ketheeswaran  

---

# 📜 License

Distributed under the MIT License.  
Feel free to use, modify, and distribute with attribution.

---

# ⭐ Support

If you found this project helpful:

- Star ⭐ the repository  
- Share with fellow developers  
- Contribute new security tools  

---

🛡️ *CyberGuard Toolkit – Empowering Ethical Cybersecurity Innovation.*
