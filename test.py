import requests, json
from pprint import pprint
from bs4 import BeautifulSoup
URL = "https://api.coingecko.com/api/v3/coins/vulcan-forged?tickers=true&market_data=true"
page = requests.get(URL)
data = json.loads(page.text)
name = data['name']
ethcontract = f"Ethereum: \n{data['platforms']['ethereum']}"
polycontract = f"Polygon: \n{data['platforms']['polygon-pos']}"
#print(data['description']['en'])
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
#print(f"Tickers: {data['tickers']}")
#b = 0
#for a in data['tickers']:
#    if b < 8:
#        URL = f"https://api.coingecko.com/api/v3/coins/{a['coin_id']}"
#        page = requests.get(URL)
#        data = json.loads(page.text)
#        coin_id = data['symbol']
#        URL = f"https://api.coingecko.com/api/v3/coins/{a['target_coin_id']}"
#        page = requests.get(URL)
#        data = json.loads(page.text)
#        target_coin_id = data['symbol']
#        print(f"{coin_id} - {target_coin_id}")
#        print(a['market']['name'])
#        print(a['converted_last']['usd'])
#        print(a['converted_volume']['usd'])
#        print(a['trade_url'])
#        b = b + 1




URL = "https://polygonscan.com/token/0x348e62131fce2f4e0d5ead3fe1719bc039b380a9?a=0x780990cf784557479fec06302bb8a53d8b0d5f43"
page = requests.get(URL)
#pprint(page.text)
soup = BeautifulSoup(page.content, "html.parser")
#results = soup.find("div", class_="card-body")
#supply = soup.find("div", class_="row align-items-center")
#results = soup.find(id="ContentPlaceHolder1_tr_valuepertoken")
#print(results.prettify())
#print(supply.text)
results = soup.find(id="ContentPlaceHolder1_tr_tokenHolders")
results = results.text.strip()
holders = f"PYR {' '.join(results.split())}"

text = f"{name}\n{ethcontract}\n{polycontract}\n{mcap}\n{mcaprank}\n{price}\n{ath}\n{volume}\n{high}\n{low}\n{change24}\n{change24perc}\n{change7dperc}\n{change30dperc}\n{maxsupply}\n{circsupply}"
print(text)
