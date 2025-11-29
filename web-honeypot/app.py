#!/usr/bin/env python3
"""
Simple Web Honeypot
Logs all HTTP requests and simulates vulnerable endpoints
"""

from flask import Flask, request, render_template_string, jsonify
import json
import logging
from datetime import datetime
import os

app = Flask(__name__)

# Configure logging
LOG_DIR = '/app/logs'
os.makedirs(LOG_DIR, exist_ok=True)

# JSON logger for structured logging
json_handler = logging.FileHandler(f'{LOG_DIR}/honeypot.json')
json_handler.setLevel(logging.INFO)

# Console logger
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

app.logger.addHandler(json_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)

def log_request():
    """Log incoming request details"""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'remote_addr': request.remote_addr,
        'method': request.method,
        'path': request.path,
        'query_string': request.query_string.decode(),
        'user_agent': request.headers.get('User-Agent', ''),
        'referer': request.headers.get('Referer', ''),
        'headers': dict(request.headers),
        'form_data': dict(request.form),
        'json_data': request.get_json(silent=True),
        'cookies': dict(request.cookies)
    }
    app.logger.info(json.dumps(log_entry))
    return log_entry

# Home page - Fake login portal
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Portal Login</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f0f0; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 300px; }
        h2 { margin-top: 0; color: #333; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .error { color: red; font-size: 14px; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>🔐 Admin Portal</h2>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}
        <p style="font-size: 12px; color: #666; margin-top: 20px;">Version 2.4.1</p>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    log_request()
    return render_template_string(HOME_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    log_entry = log_request()
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Always fail but log credentials
    app.logger.warning(f"LOGIN_ATTEMPT: username={username}, password={'*' * len(password)}")
    
    return render_template_string(HOME_TEMPLATE, error="Invalid credentials. Please try again.")

@app.route('/admin')
@app.route('/admin/')
def admin():
    log_request()
    return jsonify({"error": "Unauthorized", "code": 401}), 401

@app.route('/api/v1/status')
def api_status():
    log_request()
    return jsonify({
        "status": "online",
        "version": "1.2.3",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/v1/users')
def api_users():
    log_request()
    return jsonify({"error": "Authentication required"}), 401

# Common vulnerable endpoints
@app.route('/phpMyAdmin/')
@app.route('/phpmyadmin/')
def phpmyadmin():
    log_request()
    return "<h1>phpMyAdmin</h1><p>Error: Access denied</p>", 403

@app.route('/wp-admin/')
@app.route('/wp-login.php')
def wordpress():
    log_request()
    return "<h1>WordPress</h1><p>Page not found</p>", 404

@app.route('/.env')
def env_file():
    log_request()
    return "APP_KEY=base64:fake_key_here\nDB_PASSWORD=fake_password", 200

@app.route('/.git/config')
def git_config():
    log_request()
    return "[core]\n\trepositoryformatversion = 0", 200

# Catch-all route
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def catch_all(path):
    log_request()
    return jsonify({"error": "Not Found", "path": path}), 404

@app.errorhandler(404)
def not_found(e):
    log_request()
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(500)
def internal_error(e):
    log_request()
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
