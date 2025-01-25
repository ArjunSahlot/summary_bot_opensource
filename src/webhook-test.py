import os

import discord
from discord.ext import commands
from flask import Flask, request
import threading

# Bot setup
intents = discord.Intents.default()
intents.messages = True  # Ensure the bot can send and read messages
bot = commands.Bot(command_prefix="!", intents=intents)

# Flask setup
app = Flask(__name__)

DISCORD_CHANNEL_ID = 1332451557530402877  # Replace with your Discord channel ID


# Flask route to handle webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Parse the incoming JSON payload
    if data:
        # Extract useful information from the webhook payload
        message = data.get("message", "Default message from webhook")
        bot.loop.create_task(send_message_to_discord(message))
    return "Webhook received!", 200


# Send a message to Discord from the bot
async def send_message_to_discord(message):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print(f"Channel with ID {DISCORD_CHANNEL_ID} not found.")


# Run Flask in a separate thread
def run_flask():
    app.run(host="0.0.0.0", port=5000)  # Set host and port for the Flask server


# Run the Flask app in a thread to avoid blocking the bot
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()


# Bot events
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")


# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))

