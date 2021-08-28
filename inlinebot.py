#!/usr/bin/env python
# pylint: disable=C0116,W0613

import logging
from uuid import uuid4
import requests
import json
import pickledb
from telegram import InlineQueryResultArticle, InlineQueryResultPhoto, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
from blacklist import get_blacklist

db = pickledb.load("bot.db", True)
if not db.get("tokens"):
    db.set("tokens", [])

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("This is an inline bot. Use anywhere, in any group. Start your search by entering '@vvnftbot' followed by your search parameter. This bot supports NFT ID numbers as well as metadata text. Please note, the search is case sensitive.\n\n\nTry the following:\n@vvnftbot 15734\n@vvnftbot Asterion\n@vvnftbot Apollo\n@vvnftbot Titan\n@vvnftbot Olympian\n@vvnftbot Boreas\n@vvnftbot Notus\n@vvnftbot Hades\n@vvnftbot Arcadia\n@vvnftbot Berserk Boreas\n@vvnftbot Berserk Notus\n@vvnftbot Berserk Hades\n@vvnftbot Berserk Arcadia\n\nDeveloped by @floydvulcan")

def startjob(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Starting JobQueue!')
    context.job_queue.run_repeating(getdb, 43200)
    update.effective_chat.send_message("Job Started!")

def updatedb(update: Update, context: CallbackContext):
    getdb(context)
    update.effective_chat.send_message("DB Updated!")

def getdb(context):
    api = "http://api.vulcanforged.com/getAllArts"
    r = requests.get(api)
    data = json.loads(r.text)
    list = data['data']
    blacklist = get_blacklist()
    for a in blacklist:
        for token in list:
            if a == token['id']:
                list.remove(token)
    db.set("tokens", list)

def nft(id):
    text = ""
    count = 0
    image = "none"
    tokens = db.get("tokens")
    if id.isdigit():
        for a in tokens:
            count = count + 1
            if int(id) == a['id']:
                data = json.loads(a['ipfs_data_json'])
                text = f"NFT {id}\n"
                for key, value in data.items():
                    text = f"{text}{key} : {value}\n"
                try:
                    image = data['image']
                except:
                    pass
    else:
        count1 = 0
        text1 = ""
        for a in tokens:
            count = count + 1
            data = json.loads(a['ipfs_data_json'])
            for key, value in data.items():
                if id == 'Hippolytas Bow':
                    id = 'Hippolyta’s Bow'
                if (value == id and id != 'Berserk' and id != 'Hermes' and id != 'Trapjaw' and id != 'Zeus' and id != 'Lost Shade' and id != 'Venomtail') or (value == id and id == 'Zeus' and data['dappid'] == 8) or (value == id and id == 'Lost Shade' and data['dappid'] == 3) or (value == 'Venomtail' and id == 'Venomtail Berserk' and data['dappid'] == 11) or (value == id and id == 'Venomtail' and data['dappid'] == 3) or (value == "Trapjaw" and id == "Trapjaw" and data['dappid'] == 3) or (value == 'Trapjaw' and id == 'Trapjaw Berserk' and data['dappid'] == 11) or (value == id and id == 'Hermes' and data['dappid'] == 8):
                    count1 = count1 + 1
                    if count1 == 1:
                        try:
                            image = data['image']
                        except:
                            pass
                        for key, value in data.items():
                            text1 = f"{text1}{key} : {value}\n"
                    text = f"{text1}\nEstimated NFT Matches: {count1}"
    if text != "":
        text = f"{text}\nTotal number of VF NFTs: {count}"
    if text == "":
        text = "none"
    if image != "none":
        ipfs = f"https://cloudflare-ipfs.com/ipfs/{image}"
    if image == "none":
        ipfs = "https://vulcannfts.com/w/images/c/c8/OG_jimi-x_appreciation.jpg"

    return text, ipfs

def inlinequery(update: Update, context: CallbackContext):
    query = update.inline_query.query

    if query == "":
        return

    list = {'Boreas': ['Tomyios', 'Aelio', 'Thunder', 'Kopis', 'Asterion'],
                'Arcadia': ['Phearei', 'Alpha', 'Soter', 'Velosina', 'Chiron'],
                'Notus': ['Venomtail', 'Syna', 'Chthonius', 'Nemean', 'Numatox'],
                'Hades': ['Wolfshadow', 'Trapjaw', 'Medusa', 'Lost Shade', 'Blubberjaw', 'Charon'],
                'Olympian': ['Zeus', 'Poseidon', 'Ares', 'Hermes', 'Apollo', 'Aphrodite', 'Hera', 'Demeter'],
                'Titan': ['Cronus', 'Hyperion', 'Coeus', 'Crius', 'Iapetus', 'Oceanus', 'Rhea', 'Tethys'],
                'Berserk Arcadia': ['Sunfire Strike', 'Velosina of the Sacred Stables', 'Gift of the Great Green Ones', 'Snares of the Fae', 'Stranglevines', 'Summer Palace', 'Pipes of Pan', 'Centaur Warband', 'Summer Storms', 'Bushwhack Wolf'],
                'Berserk Boreas': ['The Fortress of Winds', 'The Breath of Boreas', "Hippolyta's Bow", 'Panoply of Minos', 'Hilltop Fort of the Amazons', 'Claws of the Harpy', 'Cantankerous Mammoth', 'Sudden Snowdrifts', 'Rip and Rend', 'Cyclops Rock Rain'],
                'Berserk Hades': ['Edge of Night', 'Cerberus, Hound of Hades', 'Funeral Barge of Acheron', 'A Storm of Strix', 'The Hymn of Thanatos', 'A Mustering of Souls', 'Sepurchral Armour', 'Javelins of Thanatos', 'Trapjaw Berserk', 'Shade Warrior'],
                'Berserk Notus': ['Blood of the Cockatrice', 'Myrmidon Warrior', 'Shield of Achilles', 'The Spear of Achilles', 'Sandstorm', 'Scorpion Stance', 'Venomtail Berserk', 'Desert Winds', 'Storm Surge', 'The Ones Who Drink']}

    results = []
    for group in list:
        if query == group:
            groupitems = list[group]
            for token in groupitems:
                text, ipfs = nft(token)
                results.append(
                    InlineQueryResultPhoto(
                        id=str(uuid4()),
                        title=token,
                        photo_url=ipfs,
                        thumb_url=ipfs,
                        caption=text,
                    )
                )

    if results == []:
        text, ipfs = nft(query)
        if text == "none":
            return
        else:
            results = [
                InlineQueryResultPhoto(
                    id=str(uuid4()),
                    title=query,
                    photo_url=ipfs,
                    thumb_url=ipfs,
                    caption=text,
                ),
            ]

    update.inline_query.answer(results, timeout=3000)

def main() -> None:
    updater = Updater("")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("startjob", startjob))
    dispatcher.add_handler(CommandHandler("updatedb", updatedb))

    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
