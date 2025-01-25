import os
from copy import deepcopy

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("src/static/summary-bot-firebase-credentials.json")
firebase_admin.initialize_app(cred)
DATABASE = firestore.client()

MAX_TOKENS = .80  # % of the max context length
INTRO_MESSAGE = """Please summarize a conversation from the discord server, '{}'. Each message in the conversations will be in the following format.

[Author]: [Message]

Apart from just normal text, there will likely also be emojis and GIFs in the message. GIFs are typically of the form 'https://tenor.com/view/[...]'. Emojis are typically of the form ':emoji_name:'. If possible, try taking these into account.
\n{}. The summary should be in {}"""
MODES = {
    "brief": "Give me a brief summary of this conversation",
    "standard": "Give me a summary of this conversation",
    "descriptive": "Give me an extremely detailed and descriptive summary of this conversation",
    "list": "Curate a list of the main points in this conversation",
    "funny": "Extract the funny parts of this conversation",
    "highlights": "Give me a summary of the highlights of this conversation",
    "important": "Give me a summary of the most important parts of this conversation",
    "controversial": "Give me a summary of the most controversial parts of this conversation",
    "spicy": "Give me a summary of the most spicy parts of this conversation. Spicy parts are those that are likely to cause arguments, or are likely to be controversial, or creating a lot of tension between people",
    "mod": "I am a discord moderator, give me a summary of the parts of the conversation I should be concerned about",
    "common words": "Dont write a paragraph summary but instead, list ONLY the 10 most common words used in the conversation at the end of the summary in bulletpoints. The bulletpoints should just consist of singular words. Going in the most to least in how many times that word occurs. Dont list out the typical common words like a or and.",
}

LINK_SUPPORT = "https://discord.gg/JBTGaKEKEc"
LINK_TOPGG = "https://top.gg/bot/1058568749076185119"
LINK_VOTE = "https://top.gg/bot/1058568749076185119/vote"
LINK_INVITE = "https://discord.com/api/oauth2/authorize?client_id=1058568749076185119&permissions=0&scope=bot%20applications.commands"

LESS_MESSAGES = "There aren't enough messages to summarize, found 0 messages apart from Summary Bot's messages."
REGION_REQUIRED = "If you want to specify a time range, you must specify a region"
START_END_TIMES = (
    "If you want to specify a time range, you must specify both a start and end time"
)
ERROR = "Summary bot has encountered an error while sending the summary. Please try again later. If this error persists, please contact the developer through the support server: https://discord.gg/JBTGaKEKEc\n\nError: {}"
HELP = """**__Main Summary Commands__**
**/summary** - Summarize a certain number of previous messages.
**/unreadsummary** - Summarize all the messages since your last sent message in a channel
**/fromtosummary** - Summarize messages between a certain time period

**__Settings Commands__**
**/listmodes** - Lists all the modes you have currently.
**/addmode** - Adds a mode to your mode list.
**/removemode** - Remove a mode from your mode list.
**/setapikey** - Set your own OpenAI API key for unlimited usage! Without this you are restricted to summarizing 2000 messages at a time. Your key stays private and secured.
**/removeapikey** - Remove your OpenAI API key from being used
**/checkserverkey** - Check if your server has an OpenAI API key set.
**/setlanguage** - Set your language that you want your summaries to be summarized in.
**/setregion** - Set your region such that you can use time-to-time summaries with your local time. Without this they would be in UTC. Your region stays private and secured.
**/setthread** - Set whether or not you want your summaries to be outputted in a thread format or a inline messages format.
**/setmodel** - Set the OpenAI model you want to use for summarization. You can choose from a variety of models with different capabilities and prices.

**__Helper Commands__**
**/ping** - Check your ping with our server.
**/help** - Get a nice help message with info about the bot.
**/invite** - Get an invite link for the bot.
**/support** - Get a link to the support server for the bot
**/vote** - Vote for the bot on top.gg!
**/update** - Check the latest big update to the bot!

If you have need support, here are some resources:
- [Support Server](https://discord.gg/JBTGaKEKEc)
- [Top.gg Page](https://top.gg/bot/1058568749076185119)
"""
GUIDE = """Hi! I'm Summary Bot, and I use AI magic to enhance your Discord experience!

**__API Key (REQUIRED)__**:
To use most of my AI features, you'll need an OpenAI API key. This will cost you a few cents per use.
- **How to set it up:** Get your API key and use `/setapikey` to add it. Personal keys are used unless a server API key is set, which takes priority.

**__Server API Keys__**:
Want to let everyone on the server summarize without needing their own key? Add a server API key!
- **How to set it up:** Get an API key, then use `/setapikey` with the server flag set to true. This key will take precedence over personal keys for all server members.

**__Customizing Summaries__**:
You can tweak summaries with **modes** and **time ranges**:

- **Modes**: Modes let you customize how prompts are sent to the AI. You can create, modify, and list modes with commands (use `/help` for details). A few default modes are already available for you to experiment with.

- **Time Ranges**: Use `/fromtosummary` to summarize specific periods, like "yesterday" or "the past hour." I’ll handle the message selection for you! Be as specific as possible to ensure I select the correct range, and double-check the time range output to confirm it’s what you intended.

**__More Features__**:
I also support model selection, thread summaries, language customization, unread message summaries, and more! Use `/help` to explore all commands and features.

**__Need Help?__**
Visit our [support server](https://discord.gg/JBTGaKEKEc) for troubleshooting, community advice, or to chat with the developer!
"""
UPDATE = "__Summary Bot Update - December 2024__\n- Fixed formatting errors in summaries\n- Added secret mode"
VOTE = f"Thanks for using Summary Bot! If you like this bot, please consider voting for it on [top.gg]({LINK_VOTE}) to help it grow."
INVITE = f"Thanks for using Summary Bot! If you like this bot, please consider inviting it to your server using [this link]({LINK_INVITE})."

SERVER_KEY_PROVIDER = "Summary Bot Key Provider"

SUMMARY_BOT_ID = 1058568749076185119

DEVELOPER_PASSWORD = r"redacted"

TIMEZONES = {
    "UTC (Universal Coordinated Time)": 0,
    "ECT+1:00 (European Central Time)": 1,
    "EET+2:00 (Eastern European Time)": 2,
    "EAT+3:00 (Eastern African Time)": 3,
    "MET+3:30 (Middle East Time)": 3.5,
    "NET+4:00 (Near East Time)": 4,
    "PLT+5:00 (Pakistan Lahore Time)": 5,
    "IST+5:30 (India Standard Time)": 5.5,
    "BST+6:00 (Bangladesh Standard Time)": 6,
    "VST+7:00 (Vietnam Standard Time)": 7,
    "CTT+8:00 (China Taiwan Time)": 8,
    "JST+9:00 (Japan Standard Time)": 9,
    "ACT+9:30 (Australia Central Time)": 9.5,
    "AET+10:00 (Australia Eastern Time)": 10,
    "NST+12:00 (New Zealand Standard)": 12,
    "HST-10:00 (Hawaii Standard Time)": -10,
    "AST-9:00 (Alaska Standard Time)": -9,
    "PST-8:00 (Pacific Standard Time)": -8,
    "MST-7:00 (Mountain Standard Time)": -7,
    "CST-6:00 (Central Standard Time)": -6,
    "EST-5:00 (Eastern Standard Time)": -5,
    "PRT-4:00 (Puerto Rico and US Virgin Islands Time)": -4,
    "CNT-3:30 (Canada Newfoundland Time)": -3.5,
    "BET-3:00 (Brazil Eastern Time)": -3,
    "CAT-1:00 (Central African Time)": -1,
}

LANGUAGES = [
    "English",
    "Spanish (Español)",
    "French (Français)",
    "German (Deutsch)",
    "Italian (Italiano)",
    "Portuguese (Português)",
    "Dutch (Nederlands)",
    "Russian (Русский)",
    "Chinese (中文)",
    "Japanese (日本語)",
    "Korean (한국어)",
    "Arabic (العربية)",
    "Hindi (हिन्दी)",
    "Bengali (বাংলা)",
    "Indonesian (Bahasa Indonesia)",
    "Swahili (Kiswahili)",
    "Turkish (Türkçe)",
    "Thai (ภาษาไทย)",
    "Vietnamese (Tiếng Việt)",
    "Polish (Polski)",
    "Swedish (Svenska)",
    "Greek (Ελληνικά)",
    "Hebrew (עִבְרִית)",
    "Danish (Dansk)",
    "Norwegian (Norsk)",
    "Finnish (Suomi)",
]

MODELS = {
    "GPT-4o Mini": {
        "name": "gpt-4o-mini",
        "description": "Our affordable and intelligent small model for fast, lightweight tasks. GPT-4o mini is cheaper and more capable than GPT-3.5 Turbo",
        "price_in": 0.15,
        "price_out": 0.6,
        "context_length": 128000,
        "cutoff": "October 2023",
    },
    "GPT-3.5 Turbo": {
        "name": "gpt-3.5-turbo",
        "description": "The latest GPT-3.5 Turbo model with higher accuracy at responding in requested formats and a fix for a bug which caused a text encoding issue for non-English language function calls.",
        "price_in": 0.5,
        "price_out": 1.5,
        "context_length": 16385,
        "cutoff": "September 2021",
    },
    "GPT-4 Turbo (Omni)": {
        "name": "gpt-4o",
        "description": "Our most advanced, multimodal flagship model that’s cheaper and faster than GPT-4 Turbo.",
        "price_in": 5,
        "price_out": 15,
        "context_length": 128000,
        "cutoff": "October 2023",
    },
    "GPT-4 Turbo": {
        "name": "gpt-4-turbo",
        "description": "The latest GPT-4 Turbo model",
        "price_in": 10,
        "price_out": 30,
        "context_length": 128000,
        "cutoff": "December 2023",
    },
    "GPT-4": {
        "name": "gpt-4",
        "description": "The original GPT-4 model",
        "price_in": 10,
        "price_out": 30,
        "context_length": 8192,
        "cutoff": "September 2021",
    }
}


MESSAGE_LINK = "https://discord.com/channels/{}/{}/{}"


def calc_cost(in_tokens, out_tokens, model):
    in_tokens = model["price_in"] * in_tokens / 1000000
    out_tokens = model["price_out"] * out_tokens / 1000000
    return round(in_tokens + out_tokens, 3)


def remove_slash(*positions):
    def wrap(func):
        def wrapper(*args):
            args = list(args)
            for p in positions:
                args[p] = str(args[p]).replace("/", "_")
            return func(*args)

        return wrapper

    return wrap


def to_dict(reference):
    return reference.get().to_dict()


@remove_slash(0)
def get_user(username):
    doc_ref = DATABASE.collection("users").document(username)
    doc_snapshot = doc_ref.get()
    if not doc_snapshot.exists:
        doc_ref.set({})

    return doc_ref


@remove_slash(0)
def set_user(username, data):
    doc_ref = DATABASE.collection("users").document(username)
    doc_ref.set(data)
    return doc_ref


@remove_slash(0, 1)
def get_server(server_name, server_id):
    doc_ref = DATABASE.collection("servers").document(f"{server_name} - {server_id}")
    doc_snapshot = doc_ref.get()
    if not doc_snapshot.exists:
        doc_ref.set({})

    return doc_ref


@remove_slash(0, 1)
def set_server(server_name, server_id, data):
    doc_ref = DATABASE.collection("servers").document(f"{server_name} - {server_id}")
    doc_ref.set(data)
    return doc_ref


@remove_slash(0, 1, 2)
def setup_user(username, server_name, server_id):
    user_ref = get_user(username)
    user = to_dict(user_ref)
    server_ref = get_server(server_name, server_id)
    server = to_dict(server_ref)

    if "servers" not in user:
        user["servers"] = [server_ref]
    else:
        if server_ref not in user["servers"]:
            user["servers"].append(server_ref)
    if "region" not in user:
        user["region"] = "UTC (Universal Coordinated Time)"
    if "language" not in user:
        user["language"] = "English"
    if "api-key" not in user:
        user["api-key"] = "NONE"
    if "model" not in user:
        user["model"] = list(MODELS.keys())[0]
    if "modes" not in user:
        user["modes"] = deepcopy(MODES)
    if "thread" not in user:
        user["thread"] = True
    if "in_token_count" not in user:
        user["in_token_count"] = 0
    if "out_token_count" not in user:
        user["out_token_count"] = 0
    if "secret_mode" not in user:
        user["secret_mode"] = False
    if "developer_mode" not in user:
        user["developer_mode"] = False

    if "users" not in server:
        server["users"] = [user_ref]
    else:
        if user_ref not in server["users"]:
            server["users"].append(user_ref)
    if "in_token_count" not in server:
        server["in_token_count"] = 0
    if "out_token_count" not in server:
        server["out_token_count"] = 0
    if "api-key" not in server:
        server["api-key"] = "NONE"
    if "secret_mode" not in server:
        server["secret_mode"] = False

    set_user(username, user)
    set_server(server_name, server_id, server)

    return user, server
