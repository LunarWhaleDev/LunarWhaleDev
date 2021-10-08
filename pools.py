import requests, json

def get_pools():
  apikey = "polygonscan api key"
  lavapyr = "0x1c6e02Dd453929b72b7377bE2F3EBdF083CcA94B"
  usdcpyr = "0x2714839101ffbbe83129247733b1f8955e917332"
  wethpyr = "0xD35f89F41C35E286624F5eD038767F4F616F32Aa"
  maticpyr = "0xA1746Cf26a0dc3272815d099156BcC2C2bAB40a2"
  pyrcontract = "0x348e62131fce2f4e0d5ead3fe1719bc039b380a9"
  lavacontract = "0xb4666B7402D287347DbBDC4EA5b30E80C376c0B3"
  usdccontract = "0x2791bca1f2de4661ed88a30c99a7a9449aa84174"
  wethcontract = "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619"
  maticcontract = "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270"
#Get lava-pyr data
  URL = f"https://api.polygonscan.com/api?module=stats&action=tokensupply&contractaddress={lavapyr}&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  lavapyrlptokens = float(data['result']) / 1000000000000000000

  URL = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={lavacontract}&address={lavapyr}&tag=latest&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  lava = float(data['result']) / 1000000000000000000

  URL = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={pyrcontract}&address={lavapyr}&tag=latest&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  pyr0 = float(data['result']) / 1000000000000000000
#Get usdc-pyr data
  URL = f"https://api.polygonscan.com/api?module=stats&action=tokensupply&contractaddress={usdcpyr}&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  usdcpyrlptokens = float(data['result']) / 1000000000000000000

  URL = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={usdccontract}&address={usdcpyr}&tag=latest&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  usdc = float(data['result']) / 1000000

  URL = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={pyrcontract}&address={usdcpyr}&tag=latest&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  pyr1 = float(data['result']) / 1000000000000000000
#Get weth-pyr data
  URL = f"https://api.polygonscan.com/api?module=stats&action=tokensupply&contractaddress={wethpyr}&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  wethpyrlptokens = float(data['result']) / 1000000000000000000

  URL = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={wethcontract}&address={wethpyr}&tag=latest&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  weth = float(data['result']) / 1000000000000000000

  URL = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={pyrcontract}&address={wethpyr}&tag=latest&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  pyr2 = float(data['result']) / 1000000000000000000
#get matic-pyr data
  URL = f"https://api.polygonscan.com/api?module=stats&action=tokensupply&contractaddress={maticpyr}&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  maticpyrlptokens = float(data['result']) / 1000000000000000000

  URL = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={maticcontract}&address={maticpyr}&tag=latest&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  matic = float(data['result']) / 1000000000000000000

  URL = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={pyrcontract}&address={maticpyr}&tag=latest&apikey={apikey}"
  r = requests.get(URL)
  data = json.loads(r.text)
  pyr3 = float(data['result']) / 1000000000000000000
#Get prices
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

  pyr1total = pyrprice * pyr1
  usdctotal = usdcprice * usdc
  usdcpyrtvl = usdctotal + pyr1total
  usdcpyrlpprice = usdcpyrtvl / usdcpyrlptokens

  pyr2total = pyrprice * pyr2
  wethtotal = wethprice * weth
  wethpyrtvl = wethtotal + pyr2total
  wethpyrlpprice = wethpyrtvl / wethpyrlptokens

  pyr3total = pyrprice * pyr3
  matictotal = maticprice * matic
  maticpyrtvl = matictotal + pyr3total
  maticpyrlpprice = maticpyrtvl / maticpyrlptokens

  text = (
    "<b>LAVA-PYR</b>\n"
    f"LP Tokens (${'{:,.2f}'.format(lavapyrlpprice)}):\n"
    f"{'{:,.2f}'.format(lavapyrlptokens)}\n"
    f"LAVA (${'{:,.2f}'.format(lavaprice)}):\n"
    f"{'{:,.2f}'.format(lava)}\n"
    f"PYR (${'{:,.2f}'.format(pyrprice)}):\n"
    f"{'{:,.2f}'.format(pyr0)}\n"
    "TVL:\n"
    f"${'{:,.2f}'.format(lavapyrtvl)}\n"
    "_____________\n"
    "<b>USDC-PYR</b>\n"
    f"LP Tokens (${'{:,.2f}'.format(usdcpyrlpprice / 1000000)} per .000001):\n"
    f"{'{:,.6f}'.format(usdcpyrlptokens)}\n"
    f"USDC (${usdcprice}):\n"
    f"{'{:,.2f}'.format(usdc)}\n"
    f"PYR (${'{:,.2f}'.format(pyrprice)}):\n"
    f"{'{:,.2f}'.format(pyr1)}\n"
    "TVL:\n"
    f"${'{:,.2f}'.format(usdcpyrtvl)}\n"
    "_____________\n"
    "<b>WETH-PYR</b>\n"
    f"LP Tokens (${'{:,.2f}'.format(wethpyrlpprice)}):\n"
    f"{'{:,.2f}'.format(wethpyrlptokens)}\n"
    f"WETH (${'{:,.2f}'.format(wethprice)}):\n"
    f"{'{:,.2f}'.format(weth)}\n"
    f"PYR (${'{:,.2f}'.format(pyrprice)}):\n"
    f"{'{:,.2f}'.format(pyr2)}\n"
    "TVL:\n"
    f"${'{:,.2f}'.format(wethpyrtvl)}\n"
    "_____________\n"
    "<b>MATIC-PYR</b>\n"
    f"LP Tokens (${'{:,.2f}'.format(maticpyrlpprice)}):\n"
    f"{'{:,.2f}'.format(maticpyrlptokens)}\n"
    f"MATIC (${'{:,.2f}'.format(maticprice)}):\n"
    f"{'{:,.2f}'.format(matic)}\n"
    f"PYR (${'{:,.2f}'.format(pyrprice)}):\n"
    f"{'{:,.2f}'.format(pyr3)}\n"
    "TVL:\n"
    f"${'{:,.2f}'.format(maticpyrtvl)}\n"
    "_____________\n"
    "<b>Total TVL</b>:\n"
    f"${'{:,.2f}'.format(lavapyrtvl + usdcpyrtvl + wethpyrtvl + maticpyrtvl)}"
  )

  return text
