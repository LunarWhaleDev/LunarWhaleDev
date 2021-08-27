#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
from uuid import uuid4
import requests
import json
import pickledb
from telegram import InlineQueryResultArticle, InlineQueryResultPhoto, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

db = pickledb.load("bot.db", True)
if not db.get("tokens"):
    db.set("tokens", [])

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def startjob(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Starting JobQueue!')
    context.job_queue.run_repeating(getdb, 60)
    update.effective_chat.send_message("Job Started!")

def updatedb(update: Update, context: CallbackContext):
    getdb(context)
    update.effective_chat.send_message("DB Updated!")

def getdb(context):
    api = "http://api.vulcanforged.com/getAllArts"
    r = requests.get(api)
    data = json.loads(r.text)
    list1 = data['data']
    db.set("tokens", list1)

def nft(update: Update, context: CallbackContext):
    if not context.args:
        return
    id = context.args[0]
    text = ""
    count = 0
    image = "none"
    tokens = db.get("tokens")
    if id.isdigit():
        for a in tokens:
            count = count + 1
            if int(id) == a['id']:
                data = json.loads(a['ipfs_data_json'])
                for key, value in data.items():
                    text = f"{text}{key} : {value}\n"
                image = data['image']
    else:
        count1 = 0
        text1 = ""
        for a in tokens:
            count = count + 1
            data = json.loads(a['ipfs_data_json'])
            for key, value in data.items():
                if value == id:
                    count1 = count1 + 1
                    try:
                        image = data['image']
                    except:
                        image = image
                    if count1 == 1:
                        for key, value in data.items():
                            text1 = f"{text1}{key} : {value}\n"
                    text = f"{text1}\nEstimated Item Count: {count1}"
    if id == "Soter":
        image = "QmY6bvjZjPaG4c1SFsQU9V2DoY5WtxywoKA2n91QZZGNdH"
    if text == "":
        text = "Invalid search\n"
        update.message.reply_text(f"{text}\nTotal number of VF NFTs: {count}")
    if image != "none":
        ipfs = f"https://cloudflare-ipfs.com/ipfs/{image}"
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=ipfs, caption=f"{text}\nTotal number of VF NFTs: {count}")
        except:
            update.message.reply_text(f"{text}\nTotal Number of VF NFTs: {count}")

def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query

    if query == "":
        return

    text = ""
    count = 0
    image = "none"
    tokens = db.get("tokens")
    if query.isdigit():
        for a in tokens:
            count = count + 1
            if int(query) == a['id']:
                data = json.loads(a['ipfs_data_json'])
                for key, value in data.items():
                    text = f"{text}{key} : {value}\n"
                image = data['image']
    else:
        count1 = 0
        text1 = ""
        for a in tokens:
            count = count + 1
            data = json.loads(a['ipfs_data_json'])
            for key, value in data.items():
                if value == query:
                    count1 = count1 + 1
                    try:
                        image = data['image']
                    except:
                        image = image
                    if count1 == 1:
                        image = data['image']
                        for key, value in data.items():
                            text1 = f"{text1}{key} : {value}\n"
                    text = f"{text1}\nEstimated Item Matches: {count1}"
    if query == "Soter":
        image = "QmY6bvjZjPaG4c1SFsQU9V2DoY5WtxywoKA2n91QZZGNdH"
    if text != "":
        text = f"{text}\nTotal number of VF NFTs: {count}"
    if text == "":
        text = f"Invalid search\n\nTotal number of VF NFTs: {count}"
    if image != "none":
        ipfs = f"https://cloudflare-ipfs.com/ipfs/{image}"

    try:
        results = [
            InlineQueryResultPhoto(
                id=str(uuid4()),
                title=query,
                photo_url=ipfs,
                thumb_url=ipfs,
                caption=text,
            ),
        ]
    except:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=query,
                input_message_content=InputTextMessageContent(text),
            ),
        ]

    update.inline_query.answer(results)

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1952808883:AAEYi9gJr_JsxPz4n2bVo4FQfrWyPFVTPoQ")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("startjob", startjob))
    dispatcher.add_handler(CommandHandler("updatedb", updatedb))
    dispatcher.add_handler(CommandHandler("nft", nft))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
