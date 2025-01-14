from discord.commands import Option
from discord.utils import basic_autocomplete

from constants import *


async def set_region(
    ctx,
    region: str = Option(
        str,
        "Region you are located in, only needed if using from/to time, stays private",
        required=True,
        autocomplete=basic_autocomplete(TIMEZONES.keys())
    ),
):
    if region not in TIMEZONES:
        await ctx.respond(f"Region `{region}` not found. Please try again with a valid region.", ephemeral=True)
        return

    user, _ = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)
    previous_region = user.get("region", "NONE")
    user["region"] = region
    set_user(str(ctx.author), user)
    await ctx.respond(f"Previous region: `{previous_region}`\nNew region: `{region}`", ephemeral=True)


async def check_server_key(ctx):
    _, server = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)
    server_key = server.get("api-key", "NONE")
    if server_key == "NONE":
        await ctx.respond(f"This server does not have a set API key :pensive:")
    else:
        await ctx.respond(f"The server has an API key set :white_check_mark:")


async def set_api_key(
    ctx,
    api_key: str = Option(
        str,
        "Your OpenAI API key (sk-***), stays private",
        required=True
    ),
    for_server: bool = Option(
        bool,
        "Whether or not you want to set this key for the entire server's use",
        default=False,
        required=True
    )
):
    user, server = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)
    if for_server:
        for role in ctx.author.roles:
            if role.name == SERVER_KEY_PROVIDER:
                previous_api_key = server.get("api-key", "NONE")
                server["api-key"] = api_key
                set_server(str(ctx.guild.name), str(ctx.guild.id), server)
                await ctx.respond(f"Previous server API key: `{previous_api_key}`\nNew server API key: `{api_key}`", ephemeral=True)
                await ctx.send(f"Updated server API key!")
                break
        else:
            await ctx.respond(f"You do not have the `{SERVER_KEY_PROVIDER}` role. Only members with this role can set a server-wide API key. Ask your moderators to give you this role.", ephemeral=True)
    else:
        previous_api_key = user.get("api-key", "NONE")
        user["api-key"] = api_key
        set_user(str(ctx.author), user)
        await ctx.respond(f"Previous user API key: `{previous_api_key}`\nNew user API key: `{api_key}`", ephemeral=True)


async def remove_api_key(
    ctx,
    for_server: bool = Option(
        bool,
        "Whether or not you want to remove the key for the entire server's use",
        default=False,
        required=True
    )
):
    user, server = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)
    if for_server:
        for role in ctx.author.roles:
            if role.name == SERVER_KEY_PROVIDER:
                previous_api_key = server.get("api-key", "NONE")
                server["api-key"] = "NONE"
                set_server(str(ctx.guild.name), str(ctx.guild.id), server)
                await ctx.respond(f"Previous server API key: `{previous_api_key}`\nNew server API key: `NONE`", ephemeral=True)
                await ctx.send(f"Server no longer has an API key :pensive:")
                break
        else:
            await ctx.respond(f"You do not have the `{SERVER_KEY_PROVIDER}` role. Only members with this role can remove the server-wide API key. Ask your moderators to give you this role.", ephemeral=True)
    else:
        previous_api_key = user.get("api-key", "NONE")
        user["api-key"] = "NONE"
        set_user(str(ctx.author), user)
        await ctx.respond(f"Previous user API key: `{previous_api_key}`\nNew user API key: `NONE`", ephemeral=True)

async def set_language(
    ctx,
    language: str = Option(
        str,
        "Language for the bot to return the summary in, stays private",
        required=True,
        default="English",
        autocomplete=basic_autocomplete(LANGUAGES)
    ),
):
    if language not in LANGUAGES:
        await ctx.respond(f"Language `{language}` not found. Please try again with a valid language.", ephemeral=True)
        return

    user, _ = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)
    previous_language = user.get("language", "NONE")
    user["language"] = language
    set_user(str(ctx.author), user)
    await ctx.respond(f"Previous language: `{previous_language}`\nNew language: `{language}`", ephemeral=True)

async def add_mode(
    ctx,
    mode_name: str = Option(str, "Name of the mode to add", required=True),
    mode: str = Option(str, "Prompt for the mode to add", required=True)
):
    user, _ = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)

    if mode_name in user["modes"]:
        await ctx.respond(f"Mode `{mode_name}` already exists. Please try again with a different mode name.", ephemeral=True)
        return
    
    if len(mode) > 1024:
        await ctx.respond(f"Mode prompt must be less than 1024 characters, you currently have {len(mode)} characters.", ephemeral=True)
        return

    user["modes"][mode_name] = mode
    set_user(str(ctx.author), user)
    await ctx.respond(f"Added mode `{mode_name}: {mode}`", ephemeral=True)

async def remove_mode(
    ctx,
    mode_name: str = Option(str, "Name of the mode to remove", required=True),
):
    user, _ = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)

    if mode_name not in user["modes"]:
        await ctx.respond(f"Mode `{mode_name}` doesn't exist. Please try again with a different mode name. Use /listmodes to see all your modes.", ephemeral=True)
        return
    
    if mode_name == "standard":
        await ctx.respond("You cannot remove the standard mode. Use /listmodes to see all your modes.", ephemeral=True)
        return

    del user["modes"][mode_name]
    set_user(str(ctx.author), user)
    await ctx.respond(f"Removed mode `{mode_name}`", ephemeral=True)

async def list_modes(
    ctx,
):
    user, _ = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)

    if len(user["modes"]) == 0:
        await ctx.respond(f"You have no modes. Use /addmode to add a mode", ephemeral=True)
        return

    modes = "\n".join([f"**{mode_name}**: {mode}" for mode_name, mode in user["modes"].items()])
    await ctx.respond(f"**__Your modes__**:\n{modes}", ephemeral=True)

async def set_thread(
    ctx,
    use_thread: bool = Option(
        bool,
        "Whether to use a thread or not",
        required=True,
        default=True
    )
):
    user, _ = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)
    previous_thread = user.get("thread", True)
    user["thread"] = use_thread
    set_user(str(ctx.author), user)
    await ctx.respond(f"Previously using thread: `{previous_thread}`\nNow using thread: `{use_thread}`", ephemeral=True)

async def set_model(
    ctx,
    model: str = Option(
        str,
        "Model to use for the bot",
        required=True,
        autocomplete=basic_autocomplete(MODELS.keys())
    ),
):
    user, _ = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)
    previous_model = user.get("model", "GPT-3.5-Turbo")
    user["model"] = model
    set_user(str(ctx.author), user)
    output = f"""
Previous model: `{previous_model}`

**New model**: **`{model}`**
**Description**: {MODELS[model]["description"]}
**Cost**: __${MODELS[model]["price_in"]}__ per 1M in tokens | __${MODELS[model]["price_out"]}__ per 1M out tokens
**Context window**: {MODELS[model]["context_length"]} tokens
**Knowledge cutoff**: {MODELS[model]["cutoff"]}
"""
    await ctx.respond(output, ephemeral=True)

async def my_cost(ctx):
    user, _ = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)
    in_tokens = user.get("in_token_count", 0)
    out_tokens = user.get("out_token_count", 0)
    cost = calc_cost(in_tokens, out_tokens, MODELS[user.get("model", "GPT-3.5-Turbo")])
    output = f"""
Your total token usage:
- Input tokens: {in_tokens}
- Output tokens: {out_tokens}
Accumulating to a total cost of approximately ``${cost}`` (calculated by GPT-3.5-Turbo Pricing)
"""
    await ctx.respond(output, ephemeral=True)

async def server_cost(ctx):
    _, server = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)
    in_tokens = server.get("in_token_count", 0)
    out_tokens = server.get("out_token_count", 0)
    cost = calc_cost(in_tokens, out_tokens, MODELS[server.get("model", "GPT-3.5-Turbo")])
    output = f"""
Total server token usage:
- Input tokens: {in_tokens}
- Output tokens: {out_tokens}
Accumulating to a total cost of approximately ``${cost}`` (calculated by GPT-3.5-Turbo Pricing)
"""
    await ctx.respond(output)

async def developer_mode(
    ctx,
    password: str = Option(
        str,
        "Password to enter developer mode",
        required=True
    )
):
    user, _ = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)
    dev_mode = user.get("developer_mode", False)
    if dev_mode:
        ctx.respond("You are already in developer mode!", ephemeral=True)
        return
    if password == DEVELOPER_PASSWORD:
        user["developer_mode"] = True
        set_user(str(ctx.author), user)
        await ctx.respond(f"Previous developer mode: `{dev_mode}`\nNew developer mode: `{True}`", ephemeral=True)
    else:
        await ctx.respond(f"Invalid password! Please try again with a valid password.", ephemeral=True)

async def costly_users(
    ctx,
    count: int = Option(
        int,
        "Number of users to display",
        default=10
    )
):
    user, _ = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)
    dev_mode = user.get("developer_mode", False)
    if not dev_mode:
        await ctx.respond(f"You are not in developer mode! Use /developermode to enter developer mode.", ephemeral=True)
    else:
        await ctx.response.defer()
        users = DATABASE.collection("users").get()
        users_with_cost = []
        for user in users:
            user = user.to_dict()
            in_tokens = user.get("in_token_count", 0)
            out_tokens = user.get("out_token_count", 0)
            users_with_cost.append((user.id, in_tokens + out_tokens*3))
        users_sorted = sorted(users_with_cost, key=lambda user: user[1], reverse=True)
        top_users = users_sorted[:count]
        output = "Top users by token count (measured in in-tokens):\n"
        output += "\n".join([f"{i+1}. **{user[0]}**: ``${user[1]}``" for i, user in enumerate(top_users)])
        await ctx.followup.send(output, ephemeral=True)

async def costly_servers(
    ctx,
    count: int = Option(
        int,
        "Number of servers to display",
        default=10
    )
):
    user, _ = setup_user(str(ctx.author), ctx.guild.name, ctx.guild.id)
    dev_mode = user.get("developer_mode", False)
    if not dev_mode:
        await ctx.respond(f"You are not in developer mode! Use /developermode to enter developer mode.", ephemeral=True)
    else:
        await ctx.response.defer()
        servers = DATABASE.collection("servers").get()
        servers_with_cost = []
        for server in servers:
            server = server.to_dict()
            in_tokens = server.get("in_token_count", 0)
            out_tokens = server.get("out_token_count", 0)
            servers_with_cost.append((server.id, in_tokens + out_tokens*3))
        servers_sorted = sorted(servers_with_cost, key=lambda server: server[1], reverse=True)
        top_servers = servers_sorted[:count]
        output = "Top servers by token count (measured in in-tokens):\n"
        output += "\n".join([f"{i+1}. **{server[0]}**: ``${server[1]}``" for i, server in enumerate(top_servers)])
        await ctx.followup.send(output, ephemeral=True)

async def ping(ctx):
    await ctx.respond(f"Latency is {round(ctx.interaction.client.latency*1000, 4)}ms")

async def update(ctx):
    await ctx.respond(UPDATE)

async def help(ctx):
    await ctx.respond(HELP)

async def guide(ctx):
    await ctx.respond(GUIDE)

async def vote(ctx):
    await ctx.respond(VOTE)

async def invite(ctx):
    await ctx.respond(INVITE)

async def info(ctx):
    try:
        guilds = ctx.bot.guilds
        num_guilds = len(guilds)
        # guild_counts = []

        # guild_ids = [guild.id for guild in guilds]
        # for guild_id in guild_ids:
        #     val = ctx.bot.fetch_guild(guild_id, with_counts=True)
        #     guild_counts.append(val.approximate_member_count)

        # member_count = sum(guild_counts)
        counts = [(guild.name, guild.id, guild.member_count) for guild in guilds]
        member_count = "{:,}".format(sum(val[2] for val in counts))
        counts = sorted(counts, key=lambda x: x[2], reverse=True)

        await ctx.respond(f"The bot is currently in {num_guilds} guilds.\nApproximate members: {member_count}\nTop Servers: {counts[0:10]}")
        
    except Exception as e:
        await ctx.respond(e)
