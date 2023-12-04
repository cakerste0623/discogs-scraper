import requests
import json
from bs4 import BeautifulSoup

discogs_username = "cakerste"

def get_ids():
    ids = []
    b = requests.get("https://api.discogs.com/users/" + discogs_username + "/wants")
    json_data = json.loads(b.text)
    wantlist = json_data["wants"]
    for wants in wantlist:
        ids.append(wants["basic_information"]["master_id"])
    return ids

def get_cheapest_listings(id):
    page = requests.get("https://www.discogs.com/sell/list?master_id=" + str(id) + "&ev=mb&ships_from=United+States&format=Vinyl&sort=price%2Casc",
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'
                        })
    return page.text

def get_lowest_price(html):
    parsed_html = BeautifulSoup(html)
    price = parsed_html.find('span', class_='price')
    return price.text

if __name__ == '__main__':
    ids = get_ids()
    for album_id in ids:
        listing = get_cheapest_listings(album_id)
        price = get_lowest_price(listing)
        price_as_float = float(price[1:])
        if price_as_float < 30:
            print(price_as_float)
