import requests
import json
from bs4 import BeautifulSoup

discogs_username = "cakerste"
conditions = ['Mint (M)', 'Near Mint (NM or M-)']

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

def send_notification(album_info):
    print(album_info)

def find_condition(html):
    for condition in conditions:
        if condition in html:
            return condition

def get_album_info(html):
    album_info = {}
    parsed_html = BeautifulSoup(html, 'html.parser')
    album_info['price'] = parsed_html.find('span', class_='price').text
    album_info['release_name'] = parsed_html.find('a', class_='item_description_title').text
    album_info['media_condition'] = find_condition(parsed_html.find('p', class_='item_condition').find('span', class_='').text)
    album_info['sleeve_condition'] = parsed_html.find('span', class_='item_sleeve_condition').text
    return album_info

if __name__ == '__main__':
    ids = get_ids()
    for album_id in ids:
        listing = get_cheapest_listings(album_id)
        album_info = get_album_info(listing)
        price_as_float = float(album_info['price'][1:])
        if price_as_float < 30:
            send_notification(album_info)
