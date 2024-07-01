import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from notion_client import Client
import json

app = Flask(__name__)
CORS(app)

# Load configuration
try:
    # First, try to load from environment variables
    integration_token = os.environ.get('NOTION_TOKEN')
    database_id = os.environ.get('DATABASE_ID')
    
    # If not found in environment, try to load from file
    if not integration_token or not database_id:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        integration_token = config["notion_token"]
        database_id = config["database_id"]
except Exception as e:
    print(f"Error loading configuration: {str(e)}")
    integration_token = None
    database_id = None

# Initialize the Notion client
try:
    notion = Client(auth=integration_token) if integration_token else None
except Exception as e:
    print(f"Error initializing Notion client: {str(e)}")
    notion = None

class DataFetcher:
    def __init__(self, notion, database_id):
        self.notion = notion
        self.database_id = database_id

    def fetch_data(self):
        try:
            response = self.notion.databases.query(database_id=self.database_id)
            return response
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return None

@app.route('/notion_integration', methods=['POST'])
def notion_integration():
    if not notion or not database_id:
        return jsonify({"error": "Notion client or database ID not properly initialized"}), 500

    try:
        data_fetcher = DataFetcher(notion, database_id)
        fetched_data = data_fetcher.fetch_data()
        if fetched_data:
            return jsonify({"processed_data": fetched_data}), 200
        else:
            return jsonify({"error": "Failed to fetch data from Notion"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Notion Integration App is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)