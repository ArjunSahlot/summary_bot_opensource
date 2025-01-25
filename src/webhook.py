from flask import Flask, request
import threading

# Flask setup
app = Flask(__name__)

channel_id = 1332451557530402877  # Replace with your Discord channel ID

# Flask route to handle webhook
@app.route('/webhook', methods=['POST'])
def webhook():

    data = request.json  # Parse the incoming JSON payload
    if data:
        # Extract useful information from the webhook payload
        message = data.get("message", "Default message from webhook") 
        app.bot.loop.create_task(send_message_to_discord(message))
    return "Webhook received!", 200

#        message = history[::-1]
#        mode = "standard"
#        secret_mode = False
#        send_summary(ctx, message, mode, channel_id, secret_mode)



# Send a message to Discord from the bot
async def send_message_to_discord(message):
    print(f"Sending {message} to {channel_id}")

    channel = app.bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        print(f"Channel with ID {channel_id} not found.")




