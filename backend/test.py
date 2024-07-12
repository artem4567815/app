""" Парсит с сайта данные для игр со стима и тех, что есть на этом сайте и строит график, но так как не подходит под все
игры и эпик пока останется не использованной """

# from datetime import datetime, timedelta
# import plotly.graph_objs as go
# import json
# from igraph.drawing.plotly.edge import plotly


# def get_price_history(game_id):
#     game_url = f"https://steampricehistory.com/app/{game_id}"
#     response = requests.get(game_url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         data = soup.find('table', class_='breakdown-table')
#         rows = data.find_all('tr')
#         price_history = []
#         for row in rows:
#             cols = row.find_all('td')
#             if len(cols) >= 4:
#                 date = cols[0].text.strip()
#                 price = cols[1].text.strip()
#                 gain = cols[2].text.strip()
#                 percent = cols[3].text.strip()
#
#                 entry = {
#                     'date': date,
#                     'price': price,
#                     'gain': gain,
#                     'percent': percent
#                 }
#                 price_history.append(entry)
#
#         return price_history
#
#
# def add_missing_months(history, id):
#     last_date_str = history[0]['date']
#     last_date = datetime.strptime(last_date_str, "%B %d, %Y")
#     current_date = datetime.now()
#     steam = Steam(os.environ.get(""))
#     user = steam.apps.get_app_details(id)
#     name = user[str(id)]['data']['name']
#     price = searching_steam(name)['apps']
#     print(price)
#     if last_date.year != current_date.year:
#         while last_date < current_date:
#             history.insert(0, {
#                 'date': last_date.strftime("%B %d, %Y"),
#                 'price': history[0]['price'],
#                 'gain': history[0]['gain'],
#                 'percent': history[0]['percent']
#             })
#             last_date += timedelta(days=30)
#         cur = current_date.strftime("%B %d, %Y").split(" ")[0]
#         months = {
#             "Январь": "01", "Февраль": "02", "Март": "03", "Апрель": "04",
#             "Май": "05", "Июнь": "06", "Июль": "07", "Август": "08",
#             "Сентябрь": "09", "Октябрь": "10", "Ноябрь": "11", "Декабрь": "12",
#             "January": "01", "February": "02", "March": "03", "April": "04",
#             "May": "05", "June": "06", "July": "07", "August": "08",
#             "September": "09", "October": "10", "November": "11", "December": "12"
#         }
#         curr = history[0]['date'].split(" ")[0]
#         if months[curr] < months[cur]:
#             history.insert(0, {
#                 'date': current_date.strftime("%B %d, %Y"),
#                 'price': price[0]['price'],
#                 'gain': history[-1]['gain'],
#                 'percent': history[-1]['percent']
#             })
#
#
# def clean_price(price_str):
#     return int(re.sub(r'[^\d.]', '', price_str))
#
#
# def doing_graph(game_id):
#     history = get_price_history(game_id)
#     add_missing_months(history, game_id)
#     data = [
#         {
#             "date": entry['date'],
#             "price": entry['price'],
#             "gain": entry['gain'] if entry['gain'] != '-' else None,
#             "percent": entry['percent']
#         }
#         for entry in reversed(history)
#     ]
#     print(data)
#     return data

import os
from steam_web_api import Steam
from epicstore_api import EpicGamesStoreAPI
import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures
from howlongtobeatpy import HowLongToBeat

#requests_cache.install_cache('game_cache', expire_after=3600)


def searching_steam(game_name, country_name):
    steam = Steam(os.environ.get(""))
    user = steam.apps.search_games(game_name, country=country_name)
    if user is None:
        return "Game Is Not Found"
    return user


# countries = {
#     "United States": "US",
#     "Russia": "RU",
#     "Great Britain": "GB",
#     "Colombia": "CO",
#     "Mexico": "MX",
#     "Poland": "PL",
#     "Republic of South Africa": "ZA",
#     "Germany": "DE",
#     "France": "FR",
#     "Spain": "ES",
#     "Denmark": "DK",
#     "Canada": "CA",
#     "Japan": "JP",
#     "Kazakhstan": "KZ",
#     "Norway": "NO",
#     "Korea": "KR",
#     "Australia": "AU",
#     "China": "CN",
#     "India": "IN",
#     "Brazil": "BR",
#     "Indonesia": "ID",
#     "Malaysia": "MY",
#     "Philippines": "PH",
#     "Singapore": "SG",
#     "Taiwan": "TW",
#     "Uruguay": "UY"
# }

countries = {
    "United States": "us",
    "Russia": "ru",
    "Great Britain": "gb",
    "Colombia": "co",
    "Mexico": "mx",
    "Poland": "pl",
    "Republic of South Africa": "za",
    "Germany": "de",
    "France": "fr",
    "Spain": "es",
    "Denmark": "dk",
    "Canada": "ca",
    "Japan": "jp",
    "Kazakhstan": "kz",
    "Norway": "no",
    "Korea": "kr",
    "Australia": "au",
    "China": "cn",
    "India": "in",
    "Brazil": "br",
    "Indonesia": "id",
    "Malaysia": "my",
    "Philippines": "ph",
    "Singapore": "sg",
    "Taiwan": "tw",
    "Uruguay": "uy"
}

API_KEY = "d4384c4b13c2b0867f9043cb1d83f31e68d860c6"


def get_game_plain(game_name):
    url = f'https://api.isthereanydeal.com/v02/game/plain/?key={API_KEY}&title={game_name}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'plain' in data['data']:
            return data['data']['plain']
    return None


def get_steam_appid(game_name):
    url = f'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        apps = data.get('applist', {}).get('apps', [])
        for app in apps:
            if game_name.lower() in app['name'].lower():
                return app['appid']
    return None


def get_game_data(game_name, country):
    appid = get_steam_appid(game_name)
    if not appid:
        return None

    url = f'https://store.steampowered.com/api/appdetails?appids={appid}&cc={country}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if str(appid) in data and data[str(appid)]['success']:
            game_info = data[str(appid)]['data']['price_overview']
            return {
                "current_price": game_info['final'] / 100,
                "initial_price": game_info['initial'] / 100,
                "discount": game_info['discount_percent'],
                "currency": game_info['currency']
            }
    return None


print(get_game_data("Terraria", "UY"))

#
#
# from flask import Flask, request, jsonify
# import requests
#
# app = Flask(__name__)
#
# API_KEY = 'd4384c4b13c2b0867f9043cb1d83f31e68d860c6'  # Замените на ваш API ключ
#
# def get_game_plain(game_name):
#     url = f'https://api.isthereanydeal.com/v02/game/plain/?key={API_KEY}&title={game_name}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         if 'plain' in data['data']:
#             return data['data']['plain']
#     return None
#
# def get_game_data(game_plain, region):
#     url = f'https://api.isthereanydeal.com/v01/game/prices/?key={API_KEY}&plains={game_plain}&region={region}'
#     response = requests.get(url)
#     print(response.text)
#     if response.status_code == 200:
#         data = response.json()
#         if game_plain in data['data']:
#             game_info = data['data'][game_plain]
#             prices = game_info['list']
#             if prices:
#                 return {
#                     "current_price": prices[0]['price_new'],
#                     "discount": prices[0]['price_cut'],
#                     "max_price": max([price['price_old'] for price in prices]),
#                     "min_price": min([price['price_new'] for price in prices]),
#                     "currency": data['.meta']["currency"]
#                 }
#     return None
#
#
# print(get_game_data(get_game_plain("Terraria"), "co"))
#

# import requests


# def searching_epic(game_name):
#     api = EpicGamesStoreAPI(locale='en-TR', country='TR')
#     search_results = api.fetch_store_games(keywords=game_name)

#     game_results = []
#     for game in search_results['data']['Catalog']['searchStore']['elements']:
#         if game_name.lower() in game['title'].lower():
#             price_info = game['price']['totalPrice']
#             print(game['price'])
#             images = game['keyImages']
#             image_url = next((img['url'] for img in images if img['type'] == 'Thumbnail'),
#                              images[0]['url'] if images else None)
#             game_info = {
#                 'name': game['title'],
#                 'epic_price': price_info['fmtPrice']['originalPrice'],
#                 'discountPrice': price_info['fmtPrice']['discountPrice'],
#                 'img': image_url,
#                 "platform": "epic",
#                 "description": game['description']
#             }
#             game_results.append(game_info)
#     return game_results


# def searching_steam(game_name):
#     steam = Steam(os.environ.get(""))
#     user = steam.apps.search_games(game_name, country="PL")
#     if user is None:
#         return "Game Is Not Found"
#     return user

# print(searching_steam("Fallout 4"))
