from constants import *

async def on_guild_join(guild):
    channel = guild.system_channel
    if channel and channel.permissions_for(guild.me).send_messages:
        await channel.send(GUIDE)

async def on_guild_remove(guild):
    print(f"\n\n\n\nKicked out of '{guild.name}'\n\n\n\n")

