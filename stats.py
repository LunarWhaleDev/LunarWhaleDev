import requests, json
from pymongo import MongoClient
import time
from datetime import datetime, timezone
import pandas as pd
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import os
from PIL import Image

mongo_client = 
db = mongo_client.dex
#db.pairs.drop()
apikey = "2BBI8S4XKAX5KNA6X8TYWRYNNYXYPI2MN7"
lavapyrcontract = "0x1c6e02Dd453929b72b7377bE2F3EBdF083CcA94B"
usdcpyrcontract = "0x2714839101ffbbe83129247733b1f8955e917332"
wethpyrcontract = "0xD35f89F41C35E286624F5eD038767F4F616F32Aa"
maticpyrcontract = "0xA1746Cf26a0dc3272815d099156BcC2C2bAB40a2"
pyrcontract = "0x348e62131fce2f4e0d5ead3fe1719bc039b380a9"
lavacontract = "0xb4666B7402D287347DbBDC4EA5b30E80C376c0B3"
usdccontract = "0x2791bca1f2de4661ed88a30c99a7a9449aa84174"
wethcontract = "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619"
maticcontract = "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270"

def get_prices(pair):
  time.sleep(1)
  URL = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={pair[1]}&address={pair[3]}&tag=latest&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  token1 = int(data['result']) / 1000000000000000000
  if pair[0] == "usdcpyr":
    token1 = int(data['result']) / 1000000
  URL = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={pair[2]}&address={pair[3]}&tag=latest&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  token2 = int(data['result']) / 1000000000000000000
  tokenexchangerate = token1 / token2
  exchangerate = [int(time.time()), tokenexchangerate]
  pairdb = db.charts.find_one({"pair": pair[0]})
  if pairdb == None:
    tokenprices = [exchangerate]
  else:
    tokenprices = pairdb['prices']
    tokenprices.append(exchangerate)
  if len(tokenprices) > 8640:
    tokenprices.pop(0)
#  print(tokenprices[-20:])
  db.charts.update_one({"pair": pair[0]}, {"$set": {"pair": pair[0], "prices": tokenprices}}, upsert=True)

#make 1d chart
  dtokenprices = tokenprices
  if len(dtokenprices) > 288:
    dtokenprices = tokenprices[-288:]
  for price in dtokenprices:
    dt_object = datetime.utcfromtimestamp(price[0])
    price[0] = dt_object.strftime("%H:%M:%S")
  df = pd.DataFrame(dict(
    time=[i[0] for i in dtokenprices],
    price=[i[1] for i in dtokenprices],
    ))
  if not os.path.exists("/home/lunarwhale/stats/static"):
    os.mkdir("/home/lunarwhale/stats/static")
  with Image.open("/home/lunarwhale/stats/static/background.jpg") as bg_image:
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
    if pair[0] == "wethpyr":
      fig.update_layout(
        yaxis_tickformat = '.5f'
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
    filename = f"/home/lunarwhale/stats/static/{pair[0]}.png"
    fig.write_image(filename)

  URL = f"https://api.polygonscan.com/api?module=stats&action=tokensupply&contractaddress={pair[3]}&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  lptokens = int(data['result']) / 1000000000000000000
  return [tokenexchangerate, token1, token2, lptokens]

def get_volume_transactions(pair):
  time.sleep(1)
  URL = f"https://api.polygonscan.com/api?module=block&action=getblocknobytime&timestamp={int(time.time())}&closest=before&apikey={apikey}"
  block = requests.get(URL)
  block = json.loads(block.text)
  block = int(block['result'])
  URL = f"https://api.polygonscan.com/api?module=account&action=tokentx&address={pair[3]}&startblock={block - 43200}&endblock={block}&sort=desc&apikey={apikey}"
  tx = requests.get(URL)
  tx = json.loads(tx.text)
  tx = tx['result']
  swaps = tx
  if len(swaps) > 30:
    swaps = tx[0:30]
  tokenswaps = []
  for swap in swaps:
    dt_object = datetime.utcfromtimestamp(int(swap['timeStamp']))
    timestamp = dt_object.strftime("%H:%M:%S")
    if swap['to'].lower() == pair[3].lower():
      address = swap['from']
      direction = "in"
    else:
      address = swap['to']
      direction = "out"
    symbol = swap['tokenSymbol']
    value = int(swap['value']) / 1000000000000000000
    if swap['tokenSymbol'] == "USDC":
      value = int(swap['value']) / 1000000
    tokenswaps.append({'timestamp': timestamp, 'address': address, 'direction': direction, 'symbol': symbol, 'value': value})
  volume = 0
  for a in tx:
    if a['tokenSymbol'] == 'PYR':
      value = int(a['value']) / 1000000000000000000
      volume = volume + value
  return [volume, tokenswaps]

def publish(data):
  data['activated'] = time.time()
  db.pairs.update_one({"pair": data['pair']}, {"$set": data}, upsert=True)
  return

#Get pair data
pair = [
  "lavapyr",
  lavacontract,
  pyrcontract,
  lavapyrcontract
  ]
lavapyrdata = get_prices(pair)
lavapyrexchange = lavapyrdata[0]
lava = lavapyrdata[1]
pyr0 = lavapyrdata[2]
lavapyrlptokens = lavapyrdata[3]
lavapyrdata = get_volume_transactions(pair)
lavapyrvolume = lavapyrdata[0]
lavapyrswaps = lavapyrdata[1]

pair = [
  "usdcpyr",
  usdccontract,
  pyrcontract,
  usdcpyrcontract
  ]
usdcpyrdata = get_prices(pair)
usdcpyrexchange = usdcpyrdata[0]
usdc = usdcpyrdata[1]
pyr1 = usdcpyrdata[2]
usdcpyrlptokens = usdcpyrdata[3]
usdcpyrdata = get_volume_transactions(pair)
usdcpyrvolume = usdcpyrdata[0]
usdcpyrswaps = usdcpyrdata[1]

pair = [
  "wethpyr",
  wethcontract,
  pyrcontract,
  wethpyrcontract
  ]
wethpyrdata = get_prices(pair)
wethpyrexchange = wethpyrdata[0]
weth = wethpyrdata[1]
pyr2 = wethpyrdata[2]
wethpyrlptokens = wethpyrdata[3]
wethpyrdata = get_volume_transactions(pair)
wethpyrvolume = wethpyrdata[0]
wethpyrswaps = wethpyrdata[1]

pair = [
  "maticpyr",
  maticcontract,
  pyrcontract,
  maticpyrcontract
  ]
maticpyrdata = get_prices(pair)
maticpyrexchange = maticpyrdata[0]
matic = maticpyrdata[1]
pyr3 = maticpyrdata[2]
maticpyrlptokens = maticpyrdata[3]
maticpyrdata = get_volume_transactions(pair)
maticpyrvolume = maticpyrdata[0]
maticpyrswaps = maticpyrdata[1]

#Get stats
URL = "https://api.coingecko.com/api/v3/simple/price?ids=vulcan-forged%2Cusd-coin%2Cweth%2Cwmatic&vs_currencies=usd"
r = requests.get(URL)
data = json.loads(r.text)
pyrprice = float(data['vulcan-forged']['usd'])
usdcprice = float(data['usd-coin']['usd'])
wethprice = float(data['weth']['usd'])
maticprice = float(data['wmatic']['usd'])

pyr0total = pyrprice * pyr0
lavaprice = pyr0total / lava
lavapyrtvl = pyr0total * 2
lavapyrlpprice = lavapyrtvl / lavapyrlptokens
lavapyrvolumeusd = lavapyrvolume * pyrprice
pair = "lavapyr"
data = {
  "pair": pair,
  "exchange_rate": lavapyrexchange,
  "lp_token_price": lavapyrlpprice,
  "lp_tokens": lavapyrlptokens,
  "lava_price": lavaprice,
  "lava_tokens": lava,
  "pyr_price": pyrprice,
  "pyr_tokens": pyr0,
  "tvl": lavapyrtvl,
  "24h_volume": lavapyrvolume,
  "24h_volume_usd": lavapyrvolumeusd,
  "recent_swaps": lavapyrswaps
  }
publish(data)

pyr1total = pyrprice * pyr1
usdctotal = usdcprice * usdc
usdcpyrtvl = usdctotal + pyr1total
usdcpyrlpprice = usdcpyrtvl / usdcpyrlptokens
usdcpyrvolumeusd = usdcpyrvolume * pyrprice
pair = "usdcpyr"
data = {
  "pair": pair,
  "exchange_rate": usdcpyrexchange,
  "lp_token_price": usdcpyrlpprice,
  "lp_tokens": usdcpyrlptokens,
  "usdc_price": usdcprice,
  "usdc_tokens": usdc,
  "pyr_price": pyrprice,
  "pyr_tokens": pyr1,
  "tvl": usdcpyrtvl,
  "24h_volume": usdcpyrvolume,
  "24h_volume_usd": usdcpyrvolumeusd,
  "recent_swaps": usdcpyrswaps
  }
publish(data)

pyr2total = pyrprice * pyr2
wethtotal = wethprice * weth
wethpyrtvl = wethtotal + pyr2total
wethpyrlpprice = wethpyrtvl / wethpyrlptokens
wethpyrvolumeusd = wethpyrvolume * pyrprice
pair = "wethpyr"
data = {
  "pair": pair,
  "exchange_rate": wethpyrexchange,
  "lp_token_price": wethpyrlpprice,
  "lp_tokens": wethpyrlptokens,
  "weth_price": wethprice,
  "weth_tokens": weth,
  "pyr_price": pyrprice,
  "pyr_tokens": pyr2,
  "tvl": wethpyrtvl,
  "24h_volume": wethpyrvolume,
  "24h_volume_usd": wethpyrvolumeusd,
  "recent_swaps": wethpyrswaps
  }
publish(data)

pyr3total = pyrprice * pyr3
matictotal = maticprice * matic
maticpyrtvl = matictotal + pyr3total
maticpyrlpprice = maticpyrtvl / maticpyrlptokens
maticpyrvolumeusd = maticpyrvolume * pyrprice
pair = "maticpyr"
data = {
  "pair": pair,
  "exchange_rate": maticpyrexchange,
  "lp_token_price": maticpyrlpprice,
  "lp_tokens": maticpyrlptokens,
  "matic_price": maticprice,
  "matic_tokens": matic,
  "pyr_price": pyrprice,
  "pyr_tokens": pyr3,
  "tvl": maticpyrtvl,
  "24h_volume": maticpyrvolume,
  "24h_volume_usd": maticpyrvolumeusd,
  "recent_swaps": maticpyrswaps
  }
publish(data)

data = {
    "pair": "all",
    "lavapyr": lavapyrexchange,
    "usdcpyr": usdcpyrexchange,
    "wethpyr": wethpyrexchange,
    "maticpyr": maticpyrexchange
    }
publish(data)
