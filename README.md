Last update: 1/13/2025

# Summary Bot - Opensource
Summary Bot's code, opensourced. This is a distinct repository from the one in active development as we have loads of private information saved in git history.

Install vscode
Install python for vscode

Install the dependencies listed in pyproject.toml
* Start a terminal in vscode
* pip install poetry
* poetry install

In vscode:
* select main.py
* start debugger



In Zapier
* Create a Zap
* Component 1:
 * Webhook
 * Get the Catch URL, e.g. "https://hooks.zapier.com/hooks/catch/1111/2f3l111/"
* Component 2:
 * Whatever you like, e.g. post to another target. e.g. a Discord channel webhook, or whatever 

In test
* Copy src/static/webhook-server-example.json your-example.json
* Edit  
{
    "history": "a set of messages to summarize",
    "bot_webhook_server": "http://localhost:5000/webhook",
    "channel_id": 1332451557530402877,
    "target_webhook": "https://hooks.zapier.com/hooks/catch/1111/2f3l111/"
}


In a command window
* cd test
* python.exe call-webhook1.py src/static/your-example.json

Expected results
* the channel number in your-example.json should be notified with the summary message
* the target_webhook should be called with the summary message

Diagnosis
* In webhook.py
* After     summary = "This is the summary of the message!"
* add breakpoints in vsCode