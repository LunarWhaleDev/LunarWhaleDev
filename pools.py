import requests, json
from bs4 import BeautifulSoup

def get_pools():
    URL = "https://polygonscan.com/address/0x2714839101ffbbe83129247733b1f8955e917332"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("ul", class_="list list-unstyled mb-0")
    list = results.find_all("li", class_="list-custom list-custom-ERC-20")
    text = '____________\n<b>USDC-PYR</b>\n'
    for a in list:
        symbol = a.find("span", class_="list-name hash-tag text-truncate")
        amount = a.find("span", class_="list-amount link-hover__item hash-tag hash-tag--md text-truncate")
        symbol = symbol.text.split()[-1].replace('(', '').replace(')', '')
        amount = float(amount.text.split()[0].replace(',', ''))
        if symbol == 'USDC':
            URL = "https://api.coingecko.com/api/v3/simple/price?ids=usd-coin&vs_currencies=usd"
            r = requests.get(URL)
            data = json.loads(r.text)
            USDC = amount * float(data['usd-coin']['usd'])
            symbolusd = float(data['usd-coin']['usd'])
        if symbol == 'PYR':
            URL = "https://api.coingecko.com/api/v3/simple/price?ids=vulcan-forged&vs_currencies=usd"
            r = requests.get(URL)
            data = json.loads(r.text)
            PYR = amount * float(data['vulcan-forged']['usd'])
            symbolusd = float(data['vulcan-forged']['usd'])
            pyrprice = symbolusd
        if symbol == 'USDC' or symbol == 'PYR':
            text = f'{text}<b>{symbol}</b> (${"{:,.2f}".format(symbolusd)})\n{"{:,.2f}".format(amount)}\n'
    text = f'{text}<b>TVL:</b>\n${"{:,.2f}".format(USDC + PYR)}\n'
    USDCPYR = USDC + PYR

    URL = "https://polygonscan.com/address/0xd35f89f41c35e286624f5ed038767f4f616f32aa"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("ul", class_="list list-unstyled mb-0")
    list = results.find_all("li", class_="list-custom list-custom-ERC-20")
    text = f'{text}____________\n<b>WETH-PYR</b>\n'
    for a in list:
        symbol = a.find("span", class_="list-name hash-tag text-truncate")
        amount = a.find("span", class_="list-amount link-hover__item hash-tag hash-tag--md text-truncate")
        symbol = symbol.text.split()[-1].replace('(', '').replace(')', '')
        amount = float(amount.text.split()[0].replace(',', ''))
        if symbol == 'WETH':
            URL = "https://api.coingecko.com/api/v3/simple/price?ids=weth&vs_currencies=usd"
            r = requests.get(URL)
            data = json.loads(r.text)
            WETH = amount * float(data['weth']['usd'])
            symbolusd = float(data['weth']['usd'])
        if symbol == 'PYR':
            PYR = amount * pyrprice
            symbolusd = pyrprice
        if symbol == 'WETH' or symbol == 'PYR':
            text = f'{text}<b>{symbol}</b> (${"{:,.2f}".format(symbolusd)})\n{"{:,.2f}".format(amount)}\n'
    text = f'{text}<b>TVL:</b>\n${"{:,.2f}".format(WETH + PYR)}\n'
    WETHPYR = WETH + PYR

    URL = "https://polygonscan.com/address/0xa1746cf26a0dc3272815d099156bcc2c2bab40a2"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("ul", class_="list list-unstyled mb-0")
    list = results.find_all("li", class_="list-custom list-custom-ERC-20")
    text = f'{text}____________\n<b>MATIC-PYR</b>\n'
    for a in list:
        symbol = a.find("span", class_="list-name hash-tag text-truncate")
        amount = a.find("span", class_="list-amount link-hover__item hash-tag hash-tag--md text-truncate")
        symbol = symbol.text.split()[-1].replace('(', '').replace(')', '')
        amount = float(amount.text.split()[0].replace(',', ''))
        if symbol == 'WMATIC':
            URL = "https://api.coingecko.com/api/v3/simple/price?ids=wmatic&vs_currencies=usd"
            r = requests.get(URL)
            data = json.loads(r.text)
            WMATIC = amount * float(data['wmatic']['usd'])
            symbolusd = float(data['wmatic']['usd'])
        if symbol == 'PYR':
            PYR = amount * pyrprice
            symbolusd = pyrprice
        if symbol == 'WMATIC' or symbol == 'PYR':
            text = f'{text}<b>{symbol}</b> (${"{:,.2f}".format(symbolusd)})\n{"{:,.2f}".format(amount)}\n'
    text = f'{text}<b>TVL:</b>\n${"{:,.2f}".format(WMATIC + PYR)}\n'
    WMATICPYR = WMATIC + PYR

    URL = "https://polygonscan.com/address/0x1c6e02dd453929b72b7377be2f3ebdf083cca94b"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("ul", class_="list list-unstyled mb-0")
    list = results.find_all("li", class_="list-custom list-custom-ERC-20")
    text = f'{text}____________\n<b>LAVA-PYR</b>\n'
    for a in list:
        symbol = a.find("span", class_="list-name hash-tag text-truncate")
        amount = a.find("span", class_="list-amount link-hover__item hash-tag hash-tag--md text-truncate")
        symbol = symbol.text.split()[-1].replace('(', '').replace(')', '')
        amount = float(amount.text.split()[0].replace(',', ''))
        if symbol == 'PYR':
            pyramount = amount
            PYR = amount * pyrprice
            symbolusd = pyrprice
        if symbol == 'LAVA':
            LAVA = amount
    text = f'{text}<b>PYR</b> (${"{:,.2f}".format(symbolusd)})\n{"{:,.2f}".format(pyramount)}\n'
    text = f'{text}<b>LAVA</b> (${"{:,.2f}".format(PYR / LAVA)})\n{"{:,.2f}".format(LAVA)}\n'
    text = f'{text}<b>TVL:</b>\n${"{:,.2f}".format(PYR * 2)}\n\n'
    LAVAPYR = PYR * 2
    text = f'{text}<b>Total TVL:</b>\n${"{:,.2f}".format(USDCPYR + WETHPYR + WMATICPYR + LAVAPYR)}'
    return text
