import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from node_modules import Sopheon

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

try:
    sopheon = Sopheon()
    logger.info("Sopheon initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Sopheon: {e}")
    sopheon = None

@app.route('/', methods=['GET'])
def home():
    return "Notion Integration App is running!"

@app.route('/notion_integration', methods=['POST'])
def notion_integration():
    if sopheon is None:
        return jsonify({"error": "Sopheon not initialized"}), 500
    
    try:
        data = request.json
        action_name = data.get('action_name')
        if action_name == 'notion_integration':
            result = sopheon.execute_custom_action(action_name)
            return jsonify({"processed_data": result}), 200
        else:
            return jsonify({"error": "Unknown action"}), 400
    except Exception as e:
        logger.error(f"Error in notion_integration: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/test_notion', methods=['GET'])
def test_notion():
    if sopheon is None:
        return jsonify({"error": "Sopheon not initialized"}), 500
    
    try:
        result = sopheon.execute_custom_action("notion_integration")
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        logger.error(f"Error in test_notion: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)