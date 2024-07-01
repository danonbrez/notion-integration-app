import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from notion_client import Client
import json

# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

logger.info("Starting application...")

# Load configuration
try:
    # First, try to load from environment variables
    integration_token = os.environ.get('NOTION_TOKEN')
    database_id = os.environ.get('DATABASE_ID')
    
    logger.info(f"Loaded from env: token={bool(integration_token)}, db_id={bool(database_id)}")
    
    # If not found in environment, try to load from file
    if not integration_token or not database_id:
        logger.info("Attempting to load from config file...")
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        integration_token = config["notion_token"]
        database_id = config["database_id"]
        logger.info("Loaded from config file")
except Exception as e:
    logger.error(f"Error loading configuration: {str(e)}")
    integration_token = None
    database_id = None

# Initialize the Notion client
try:
    notion = Client(auth=integration_token) if integration_token else None
    logger.info(f"Notion client initialized: {bool(notion)}")
except Exception as e:
    logger.error(f"Error initializing Notion client: {str(e)}")
    notion = None

class DataFetcher:
    def __init__(self, notion, database_id):
        self.notion = notion
        self.database_id = database_id

    def fetch_data(self):
        try:
            logger.info("Attempting to fetch data from Notion...")
            response = self.notion.databases.query(database_id=self.database_id)
            logger.info("Data fetched successfully")
            return response
        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}")
            return None

@app.route('/notion_integration', methods=['POST'])
def notion_integration():
    logger.info("Received request to /notion_integration")
    if not notion or not database_id:
        logger.error("Notion client or database ID not properly initialized")
        return jsonify({"error": "Notion client or database ID not properly initialized"}), 500

    try:
        data_fetcher = DataFetcher(notion, database_id)
        fetched_data = data_fetcher.fetch_data()
        if fetched_data:
            logger.info("Successfully fetched and processed data")
            return jsonify({"processed_data": fetched_data}), 200
        else:
            logger.error("Failed to fetch data from Notion")
            return jsonify({"error": "Failed to fetch data from Notion"}), 500
    except Exception as e:
        logger.error(f"Error in notion_integration: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    logger.info("Received request to home route")
    return "Notion Integration App is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port)

logger.info("Application setup complete")