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
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
#    update.message.reply_text('Help!')
    if not context.args:
        print("no args")
        return

    id = context.args[0]
    if id.isdigit():
        api = f"http://api.vulcanforged.com/getArtByID/{id}"
        r = requests.get(api)
        data = json.loads(r.text)
        list = data['data']
        text = ""
        image = list['image']
        for key, value in list.items():
            text = f"{text}{key} : {value}\n"
#        print(key, ' : ', value)
        update.message.reply_text(text)
        ipfs = f"https://cloudflare-ipfs.com/ipfs/{image}"
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=ipfs)

    else:
        api = "https://api.vulcanforged.com/getTokenByDappid/3"
        r = requests.get(api)
        data = json.loads(r.text)
        list1 = data['data']
#        print(list1[0])
#        print(list1[1])
#        return
        api = "https://api.vulcanforged.com/getTokenByDappid/8"
        r = requests.get(api)
        data = json.loads(r.text)
        list2 = data['data']
        list1.extend(list2)
#        print(list1[0])
#        print(list1[-1])
        count = 0
        for nft in list1:
            data = nft['ipfs_data_json']
            data = json.loads(data)
            for key, value in data.items():
                if value == id:
#                    print(key, " : ", value)
                    if count == 0:
                        text = ""
                        image = data['image']
                        for key, value in data.items():
                            text = f"{text}{key} : {value}\n"
#                    print(text)
                    count = count + 1
        update.message.reply_text(f"{text}Estimated count:{count}")
        ipfs = f"https://cloudflare-ipfs.com/ipfs/{image}"
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=ipfs)
#                    print(count)


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query

    if query == "":
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"_{escape_markdown(query)}_", parse_mode=ParseMode.MARKDOWN
            ),
        ),
    ]

    if query.isdigit():
        results = []
    update.inline_query.answer(results)


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1952808883:AAEYi9gJr_JsxPz4n2bVo4FQfrWyPFVTPoQ")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

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
