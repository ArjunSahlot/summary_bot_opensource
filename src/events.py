from constants import *

async def on_guild_join(guild):
    print(f"\n\n\n\nJoined '{guild.name}'\n\n\n\n")

async def on_guild_remove(guild):
    print(f"\n\n\n\nKicked out of '{guild.name}'\n\n\n\n")

