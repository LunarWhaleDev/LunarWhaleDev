import logging
import pandas as pd
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import requests, json
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import os
from PIL import Image
import telegram
from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import CommandHandler

TOKEN = ''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def markets(update, context):
    URL = "https://api.coingecko.com/api/v3/coins/vulcan-forged?tickers=true&market_data=true"
    page = requests.get(URL)
    data = json.loads(page.text)
    text = ""
    b = 0
    for a in data['tickers']:
        if b < 8:
            URL = f"https://api.coingecko.com/api/v3/coins/{a['coin_id']}"
            page = requests.get(URL)
            data = json.loads(page.text)
            coin_id = data['symbol'].upper()
            URL = f"https://api.coingecko.com/api/v3/coins/{a['target_coin_id']}" 
            page = requests.get(URL)
            data = json.loads(page.text)
            target_coin_id = data['symbol'].upper()
            rtext = f"<b>{coin_id} - {target_coin_id}</b>\n<a href='{a['trade_url']}'>{a['market']['name']}</a>\nPrice: ${a['converted_last']['usd']}\nVolume: ${a['converted_volume']['usd']}\n\n"
            text = text + rtext
            b = b + 1
    context.bot.send_message(update.message.chat_id, text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

def price(update, context):
    URL = "https://api.coingecko.com/api/v3/coins/vulcan-forged?tickers=true&market_data=true"
    page = requests.get(URL)
    data = json.loads(page.text)
    text = f"${data['market_data']['current_price']['usd']}"
    update.effective_chat.send_message(text)

def stats(update, context):
    URL = "https://api.coingecko.com/api/v3/coins/vulcan-forged?tickers=true&market_data=true" 
    page = requests.get(URL)
    data = json.loads(page.text)
    name = f"PYR - {data['name']}"
    ethcontract = f"Ethereum: \n{data['platforms']['ethereum']}"
    polycontract = f"Polygon: \n{data['platforms']['polygon-pos']}"
    mcaprank = f"Market Cap Rank: {data['market_cap_rank']}"
    mcap = f"Market Cap: ${data['market_data']['market_cap']['usd']}"
    price = f"Current Price: ${data['market_data']['current_price']['usd']}"
    ath = f"ATH: ${data['market_data']['ath']['usd']}"
    volume = f"Total Volume: ${data['market_data']['total_volume']['usd']}"
    high = f"24H High: ${data['market_data']['high_24h']['usd']}"
    low = f"24H Low: ${data['market_data']['low_24h']['usd']}"
    change24 = f"24H Price Change: ${data['market_data']['price_change_24h']}" 
    change24perc = f"24H Change Percentage: {data['market_data']['price_change_percentage_24h']}%"
    change7dperc = f"7D Change Percentage: {data['market_data']['price_change_percentage_7d']}%"
    change30dperc = f"30D Change Percentage: {data['market_data']['price_change_percentage_30d']}%"
    maxsupply = f"Max Supply: {data['market_data']['max_supply']}"
    circsupply = f"Circulating Supply: {data['market_data']['circulating_supply']}"
    URL = "https://polygonscan.com/token/0x348e62131fce2f4e0d5ead3fe1719bc039b380a9?a=0x780990cf784557479fec06302bb8a53d8b0d5f43" 
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="ContentPlaceHolder1_tr_tokenHolders")
    results = results.text.strip()
    holders = f"PYR {' '.join(results.split())}"
    text = f"{name}\n{ethcontract}\n{polycontract}\n{mcap}\n{mcaprank}\n{price}\n{ath}\n{volume}\n{high}\n{low}\n{change24}\n{change24perc}\n{change7dperc}\n{change30dperc}\n{maxsupply}\n{circsupply}"
    update.effective_chat.send_message(text)

def save_chart():
    r =  requests.get('https://api.coingecko.com/api/v3/coins/vulcan-forged/market_chart?vs_currency=usd&days=1')
    r_prices = r.json().get('prices')
    for price in r_prices:
        dt_object = datetime.utcfromtimestamp(price[0]/1000)
        price[0] = dt_object.strftime("%H:%M:%S")
    df = pd.DataFrame(dict(
        time=[i[0] for i in r_prices],
        price=[i[1] for i in r_prices],
        ))
    if not os.path.exists("images"):
        os.mkdir("images")
    with Image.open("images/background.jpg") as bg_image:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['time'], y=df['price'], line=dict(width=6), mode='lines'))
        fig.update_layout(
            plot_bgcolor='#212529',
            paper_bgcolor='#212529',
            yaxis_title='Price',
            xaxis_title='Last 24h',
            xaxis_showgrid=False,
            xaxis_showticklabels=False,
            yaxis_gridcolor='#f55d1e',
            yaxis_tickformat = '.2f',
            yaxis_linecolor='#f55d1e',
            yaxis=dict(color="#f55d1e"),
            xaxis=dict(color="#f55d1e"),
            height=512,
            width=1052,
            margin=dict(r=0, l=10, b=10, t=0),
            font=dict(size=24)
        )
        fig.add_layout_image(
            dict(source=bg_image,
                xref="paper",
                yref="paper",
                x=0.22,
                y=1,
                sizex=1,
                sizey=1,
                sizing="contain",
                opacity=0.5,
                layer="below")
        )
        fig.write_image("images/fig1.png")

def chart(update, context):
    chat_id = update.effective_chat.id
    save_chart()
    context.bot.send_photo(chat_id, photo=open('images/fig1.png', 'rb'))

def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    # The chart function will be called when someone types /chart
    dispatcher.add_handler(CommandHandler("chart", chart))
    dispatcher.add_handler(CommandHandler("c", chart))
    dispatcher.add_handler(CommandHandler("price", price))
    dispatcher.add_handler(CommandHandler("p", price))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("markets", markets))
    # Start listening for chat commands
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
