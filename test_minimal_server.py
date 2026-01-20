#!/usr/bin/env python3
"""
Test Minimal Server
"""
from flask import Flask, request, jsonify
import os
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return "Server OK"

@app.route('/api/search', methods=['POST'])
def search_product():
    try:
        query = request.json.get('query', '')
        page = request.json.get('page', 1)
        
        # Log to file
        with open('api_search_called.txt', 'w') as f:
            f.write(f"CALLED! Query={query}, Page={page}\n")
        
        # Return test data
        return jsonify({'count': 99, 'articles': [], 'query': query, 'page': page})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting minimal server...")
    app.run(host='0.0.0.0', port=3000, debug=False)
