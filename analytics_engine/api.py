from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from ingest_garmin import fetch_garmin_data

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/api/sync', methods=['POST'])
def sync_garmin():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email and password are required'}), 400
    
    try:
        logger.info(f"Starting sync for user: {email}")
        # Run ingestion logic
        fetch_garmin_data(email, password)
        
        # TODO: Run K-Means analysis here
        
        return jsonify({'status': 'success', 'message': 'Synced runs and updated profile'}), 200
        
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        # Check for auth error specifically if possible, but generic 401/500 for now
        if "authentication" in str(e).lower() or "login" in str(e).lower():
             return jsonify({'status': 'error', 'message': 'Authentication failed'}), 401
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)



