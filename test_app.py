"""Simple test app"""
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/logs', methods=['GET', 'POST'])
def get_logs():
    """Test logs endpoint"""
    password = request.args.get('password') if request.method == 'GET' else (request.json.get('password') if request.json else None)
    
    if password == 'tg':
        return jsonify({'status': 'SUCCESS', 'message': 'Password correct!', 'logs': ['entry1', 'entry2']})
    else:
        return jsonify({'error': 'Mot de passe incorrect', 'password_received': password}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
