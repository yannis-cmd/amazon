"""Run app_web_v2_1 with Waitress"""
from app_web_v2_1 import app

# Test route to confirm this module is loaded
@app.route('/test-appserver')
def test_appserver():
    return {'status': 'appserver.py loaded successfully'}

if __name__ == '__main__':
    app.run(port=3000)
