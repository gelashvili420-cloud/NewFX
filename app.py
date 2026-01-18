from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()

def fetch_html(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    return requests.get(url, headers=headers).text

# ========= Valuto ===========
def parse_valuto():
    html = fetch_html("https://valuto.ge/valutis-konvertacia/")
    soup = BeautifulSoup(html, "html.parser")
    data = {}
    blocks = soup.select("div.currency-item")
    for b in blocks:
        try:
            code = b.select_one("div.currency-name").text.strip().split()[0]
            buy = b.select_one("div.buy").text.strip()
            sell = b.select_one("div.sell").text.strip()
            data[code] = {"buy": buy, "sell": sell}
        except:
            pass
    return data

# ========= Rico ===========
def parse_rico():
    html = fetch_html("https://rico.ge")
    soup = BeautifulSoup(html, "html.parser")
    data = {}
    rows = soup.select("tr.currency-row")
    for r in rows:
        cols = r.find_all("td")
        if len(cols) >= 3:
            code = cols[0].text.strip()
            buy = cols[1].text.strip()
            sell = cols[2].text.strip()
            data[code] = {"buy": buy, "sell": sell}
    return data

# ========= MJC ===========
def parse_mjc():
    html = fetch_html("https://mjc.ge/rates")
    soup = BeautifulSoup(html, "html.parser")
    data = {}
    rows = soup.select("table tr")
    for r in rows:
        cols = r.find_all("td")
        if len(cols) >= 3:
            code = cols[0].text.strip()
            buy = cols[1].text.strip()
            sell = cols[2].text.strip()
            data[code] = {"buy": buy, "sell": sell}
    return data

# ========= Kursi.ge ===========
def parse_kursi():
    html = fetch_html("https://kursi.ge/ka/")
    soup = BeautifulSoup(html, "html.parser")
    data = {}
    rows = soup.select("table tr")
    for r in rows:
        cols = r.find_all("td")
        if len(cols) >= 3:
            code = cols[0].text.strip()
            buy = cols[1].text.strip()
            sell = cols[2].text.strip()
            if code:
                data[code] = {"buy": buy, "sell": sell}
    return data

# ========= GiroCredit ===========
def parse_giro():
    html = fetch_html("https://girocredit.ge/web/")
    soup = BeautifulSoup(html, "html.parser")
    data = {}
    rows = soup.select("table tr")
    for r in rows:
        cols = r.find_all("td")
        if len(cols) >= 4:
            code = cols[0].text.strip()
            buy = cols[1].text.strip()
            sell = cols[2].text.strip()
            if code:
                data[code] = {"buy": buy, "sell": sell}
    return data

# ========= ExpressLombard ===========
def parse_express():
    html = fetch_html("https://expresslombard.ge/ka/valutis-kursebi")
    soup = BeautifulSoup(html, "html.parser")
    data = {}
    rows = soup.select("h3")
    for r in rows:
        txt = r.text.strip()
        if txt:
            try:
                parts = r.find_next_siblings("h4")
                official = parts[0].text.strip()
                buy = parts[1].text.strip()
                sell = parts[2].text.strip()
                data[txt] = {"official": official, "buy": buy, "sell": sell}
            except:
                pass
    return data

# ========= Crystal.ge ===========
def parse_crystal():
    html = fetch_html("https://crystal.ge/valutis-kursebi/")
    soup = BeautifulSoup(html, "html.parser")
    data = {}
    rows = soup.select("div.rate-item")
    for r in rows:
        try:
            code = r.select_one("div.currency-code").text.strip()
            buy = r.select_one("div.buy").text.strip()
            sell = r.select_one("div.sell").text.strip()
            data[code] = {"buy": buy, "sell": sell}
        except:
            pass
    return data

@app.get("/rates")
def all_rates():
    return {
        "valuto": parse_valuto(),
        "rico": parse_rico(),
        "mjc": parse_mjc(),
        "kursi": parse_kursi(),
        "giro": parse_giro(),
        "express": parse_express(),
        "crystal": parse_crystal()
    }
