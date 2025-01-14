import os
import json
import threading

import discord
from dotenv import load_dotenv
load_dotenv()

from summary import summary, fromtosummary, unreadsummary
from deployment import server
from constants import *
from events import *
from commands import *


intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

async def on_ready():
    print(f"{bot.user.name} is ready")

bot.event(on_ready)
bot.event(on_guild_join)
bot.event(on_guild_remove)

bot.slash_command(name="summary", description="Get a summary of the last messages in this channel")(summary)
bot.slash_command(name="fromtosummary", description="Get a summary from a certain time to a certain time")(fromtosummary)
bot.slash_command(name="unreadsummary", description="Get a summary of all the messages after your last sent message")(unreadsummary)

bot.slash_command(name="setregion", description="Set your region (required for from/to time)")(set_region)
bot.slash_command(name="setlanguage", description="Set your language for future summaries")(set_language)
bot.slash_command(name="setthread", description="Choose whether or not you want to use a thread for summaries")(set_thread)

bot.slash_command(name="checkserverkey", description="Check whether or not the server has a set API key")(check_server_key)
bot.slash_command(name="setapikey", description="Set your OpenAI API key to use with the bot")(set_api_key)
bot.slash_command(name="removeapikey", description="Remove your OpenAI API key")(remove_api_key)
bot.slash_command(name="setmodel", description="Set the OpenAI model to use for future summaries")(set_model)

bot.slash_command(name="addmode", description="Add a mode to use for future summaries")(add_mode)
bot.slash_command(name="removemode", description="Remove an existing mode")(remove_mode)
bot.slash_command(name="listmodes", description="List your existing modes")(list_modes)

bot.slash_command(name="mycost", description="Checkout how much you have cost Summary Bot!")(my_cost)
bot.slash_command(name="servercost", description="Checkout how much this server has cost Summary Bot!")(server_cost)

bot.slash_command(name="developermode", description="Enter developer mode!")(developer_mode)
bot.slash_command(name="costlyusers", description="Developer only!")(costly_users)
bot.slash_command(name="costlyservers", description="Developer only!")(costly_servers)

bot.slash_command(name="ping", description="Check the bot's latency")(ping)
bot.slash_command(name="update", description="What's new in the latest update")(update)
bot.slash_command(name="help", description="Get help with the bot")(help)
bot.slash_command(name="guide", description="Guide to summary bot")(guide)
bot.slash_command(name="vote", description="Vote for the bot!")(vote)
bot.slash_command(name="invite", description="Invite the bot to your server")(invite)
bot.slash_command(name="info", description="Info about the bot")(info)



if __name__ == "__main__":
    threading.Thread(target=server.serve_forever).start()
    print("Server started on port 8000")

    bot.run(os.getenv("DISCORD_TOKEN"))
