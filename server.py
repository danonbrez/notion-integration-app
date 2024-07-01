from flask import Flask, jsonify
from notion_client import Client
import os

app = Flask(__name__)

# Load configuration from environment variables
notion_token = os.getenv('NOTION_TOKEN')
database_id = os.getenv('DATABASE_ID')

# Initialize Notion client
notion = Client(auth=notion_token)

class DataFetcher:
    def __init__(self, notion, database_id):
        self.notion = notion
        self.database_id = database_id

    def fetch_data(self):
        response = self.notion.databases.query(database_id=self.database_id)
        return response

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    data_fetcher = DataFetcher(notion, database_id)
    fetched_data = data_fetcher.fetch_data()
    return jsonify(fetched_data)

if __name__ == '__main__':
    app.run(debug=True)