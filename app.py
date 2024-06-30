from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/notion_integration', methods=['POST'])
def notion_integration():
    try:
        data = request.json
        action_name = data.get('action_name')
        if action_name == 'notion_integration':
            # Call the function to fetch and process data
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
    app.run(debug=True)