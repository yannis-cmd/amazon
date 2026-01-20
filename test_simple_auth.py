#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/logs', methods=['GET', 'POST'])
def test_logs():
    ADMIN_PASSWORD = "tg"
    password = ''
    
    print(f"\n--- Request Details ---")
    print(f"Method: {request.method}")
    print(f"Content-Type: {request.content_type}")
    print(f"Data: {request.data}")
    
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.data.decode('utf-8'))
            print(f"Parsed JSON: {data}")
            password = data.get('password', '')
        except Exception as e:
            print(f"JSON Error: {e}")
            password = request.args.get('password', '')
    else:
        password = request.args.get('password', '')
    
    print(f"Password extracted: '{password}'")
    print(f"Expected: '{ADMIN_PASSWORD}'")
    
    password = password.strip().lower() if password else ''
    print(f"After normalization: '{password}'")
    print(f"Match: {password == ADMIN_PASSWORD.lower()}")
    print("---")
    
    if password != ADMIN_PASSWORD.lower():
        return jsonify({'error': 'Mot de passe incorrect', 'received': password}), 401
    
    return jsonify({'success': True, 'password': password})

if __name__ == '__main__':
    from waitress import serve
    print("Starting test server on port 3001...")
    serve(app, host='0.0.0.0', port=3001)
