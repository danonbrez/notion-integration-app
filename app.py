import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/', methods=['GET'])
def home():
    return "Hello, World!"

@app.route('/notion_integration', methods=['POST'])
def notion_integration():
    try:
        data = request.json
        action_name = data.get('action_name')
        if action_name == 'notion_integration':
            result = {
                "processed_title": "SAMPLE NOTION DATA",
                "processed_content": "This is a sample content fetched from notion database."
            }
            return jsonify(result), 200
        else:
            return jsonify({"error": "Unknown action"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)