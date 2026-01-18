from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()

def get_valuto():
    url = "https://valuto.ge/valutis-konvertacia/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    data = {}
    blocks = soup.select("div.currency-item")
    for b in blocks:
        code = b.select_one("div.currency-name").text.strip().split()[0]
        buy = b.select_one("div.buy").text.strip()
        sell = b.select_one("div.sell").text.strip()
        data[code] = {"buy": buy, "sell": sell}
    return data

def get_kursi():
    url = "https://kursi.ge/ka/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    data = {}
    rows = soup.select("div.exchange-rate")
    for r in rows:
        code = r.select_one("div.currency-code").text.strip()
        buy = r.select_one("div.buy").text.strip()
        sell = r.select_one("div.sell").text.strip()
        data[code] = {"buy": buy, "sell": sell}
    return data

def get_giro():
    url = "https://girocredit.ge/web/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    data = {}
    rows = soup.select("table tbody tr")
    for r in rows:
        cols = r.find_all("td")
        if len(cols) >= 4:
            code = cols[0].text.strip()
            buy = cols[1].text.strip()
            sell = cols[2].text.strip()
            data[code] = {"buy": buy, "sell": sell}
    return data

def get_express():
    url = "https://expresslombard.ge/ka/valutis-kursebi"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    data = {}
    rows = soup.select("div.currency-block")
    for r in rows:
        code = r.select_one("div.currency-title").text.strip()
        buy = r.select_one("div.buy").text.strip()
        sell = r.select_one("div.sell").text.strip()
        data[code] = {"buy": buy, "sell": sell}
    return data

def get_crystal():
    url = "https://crystal.ge/valutis-kursebi/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    data = {}
    rows = soup.select("div.rate-item")
    for r in rows:
        code = r.select_one("div.currency-code").text.strip()
        buy = r.select_one("div.buy").text.strip()
        sell = r.select_one("div.sell").text.strip()
        data[code] = {"buy": buy, "sell": sell}
    return data

def get_rico():
    url = "https://rico.ge"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    data = {}
    rows = soup.select("tr.currency-row")
    for r in rows:
        cols = r.find_all("td")
        code = cols[0].text.strip()
        buy = cols[1].text.strip()
        sell = cols[2].text.strip()
        data[code] = {"buy": buy, "sell": sell}
    return data

def get_mjc():
    url = "https://mjc.ge/rates"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    data = {}
    rows = soup.select("table tbody tr")
    for r in rows:
        cols = r.find_all("td")
        if len(cols) >= 3:
            code = cols[0].text.strip()
            buy = cols[1].text.strip()
            sell = cols[2].text.strip()
            data[code] = {"buy": buy, "sell": sell}
    return data

@app.get("/rates")
def rates():
    return {
        "valuto": get_valuto(),
        "kursi": get_kursi(),
        "giro": get_giro(),
        "express": get_express(),
        "crystal": get_crystal(),
        "rico": get_rico(),
        "mjc": get_mjc()
    }
