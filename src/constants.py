import os
from copy import deepcopy
import firebase_admin
from firebase_admin import firestore, credentials

cred = credentials.Certificate(
    "static/summary-bot-firebase-credentials.json"
)
firebase_admin.initialize_app(cred)
DATABASE = firestore.client()

MAX_TOKENS = 3620
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
START_END_TIMES = "If you want to specify a time range, you must specify both a start and end time"
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
UPDATE = "Unfortunately due to inappropriate usage of the common API key provided by Summary Bot, we have decided to shut it down. Summary Bot is still fully functional, but just with your own OpenAI API key.\n\nOther updates:\n- TTS is now much more stable and will not crash for large summaries\n- To battle the lack of a common API key, Summary Bot now supports server-wide API keys! Set it up with the `/setapikey` command, remember to set `for_server` to True!"
VOTE = f"Thanks for using Summary Bot! If you like this bot, please consider voting for it on [top.gg]({LINK_VOTE}) to help it grow."
INVITE = f"Thanks for using Summary Bot! If you like this bot, please consider inviting it to your server using [this link]({LINK_INVITE})."

SERVER_KEY_PROVIDER = "Summary Bot Key Provider"

SUMMARY_BOT_ID = 1058568749076185119

DEVELOPER_PASSWORD = r"jsd0f=*sdnfkOD0S&2h"

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

MESSAGE_LINK = "https://discord.com/channels/{}/{}/{}"

def calc_cost(in_tokens, out_tokens):
    return round(0.0015*(in_tokens/1000) + 0.02*(out_tokens/1000), 5)

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
    if "modes" not in user:
        user["modes"] = deepcopy(MODES)
    if "thread" not in user:
        user["thread"] = True
    if "in_token_count" not in user:
        user["in_token_count"] = 0
    if "out_token_count" not in user:
        user["out_token_count"] = 0
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

    set_user(username, user)
    set_server(server_name, server_id, server)

    return user, server
