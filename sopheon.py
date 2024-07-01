from notion_client import Client
import json

# Load configuration
with open('config_corrected.json.txt', 'r') as config_file:
    config = json.load(config_file)

integration_token = config["notion_token"]
database_id = config["database_id"]

# Initialize the Notion client
notion = Client(auth=integration_token)

class DataFetcher:
    def __init__(self, notion, database_id):
        self.notion = notion
        self.database_id = database_id

    def fetch_data(self):
        response = self.notion.databases.query(
            database_id=self.database_id
        )
        return response

# Instantiate DataFetcher and fetch data
data_fetcher = DataFetcher(notion, database_id)
fetched_data = data_fetcher.fetch_data()

print(fetched_data)