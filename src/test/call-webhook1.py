import requests

import json
import sys

if len(sys.argv) != 2:
    print("Usage: python call-webhook1.py <config_file>")
    sys.exit(1)

config_file = sys.argv[1] # e.g. "src/static/martin.json"

# Read configuration values from martin.json
with open(config_file, 'r') as config_file:
    config = json.load(config_file)

url = config['bot_webhook_server']
headers = {"Content-Type": "application/json"}
payload = {
    "message": config['history'],
    "channel_id": config['channel_id'],
    "target_webhook": config['target_webhook']
}


 
# Define the URL and payload

headers = {"Content-Type": "application/json"}


# Make the POST request
response = requests.post(url, headers=headers, json=payload)

# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")
