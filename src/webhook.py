from datetime import datetime

from flask import Flask, request
import threading
#import summary
import requests

# Flask setup
app = Flask(__name__)


# Flask route to handle webhook
@app.route('/webhook', methods=['POST'])
def webhook():

    data = request.json  # Parse the incoming JSON payload
    if data:
        # Extract useful information from the webhook payload
        message = data.get("message", "Default message from webhook") 
        target_channel_id = data.get("target_channel_id", 0)
        if target_channel_id == 0:
            target_channel_id = int(target_channel_id)
        target_webhook = data.get("target_webhook", 0)
        app.bot.loop.create_task(send_message_to_discord(message, target_channel_id))
        app.bot.loop.create_task(call_for_summary(message, "standard", target_channel_id, False, target_webhook))

#        message = history[::-1]
#        mode = "standard"
#        secret_mode = False
#        send_summary(ctx, message, mode, channel_id, secret_mode)
        #app.bot.loop.create_task(send_summary(ctx, message, mode, channel_id, secret_mode))

    return "Webhook received!", 200

# Send a message to Discord from the bot
async def send_message_to_discord(message, channel_id):
    print(f"Sending {message} to {channel_id}")

    channel = app.bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        print(f"Channel with ID {channel_id} not found.")


async def call_for_summary(message, mode, channel_id, secret_mode, target_webhook):
    print(f"Calling for summary of {message} in {mode} mode")
    summary = "This is the summary of the message!"
    await send_message_to_discord(summary, channel_id)
    await send_message_to_webhook(summary, target_webhook)


async def send_message_to_webhook(message, target_webhook):
    print(f"Sending {message} to {target_webhook}")

    if not target_webhook:
        print("No target webhook provided.")
        return

    headers = {"Content-Type": "application/json"}
    payload = {"content": message,
               "timestamp": datetime.now().isoformat()
               }
    response = requests.post(target_webhook, headers=headers, json=payload)
    print(f"Webhook response: {response.status_code}")

