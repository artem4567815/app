import os
from steam_web_api import Steam
from epicstore_api import EpicGamesStoreAPI
import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures
from functools import lru_cache
import requests_cache


steam_key = ""

requests_cache.install_cache('game_cache', expire_after=3600)


def normalize_game_name(game_name):
    return re.sub(r'\W+', '', game_name.lower()) if game_name[-1] != "+" else game_name


@lru_cache(maxsize=100)
def get_game_image_from_steam(game_name):
    search_url = f"https://store.steampowered.com/search/?term={game_name.replace(' ', '+')}"

    response = requests.get(search_url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        first_result = soup.find('a', class_='search_result_row')

        if first_result:
            game_url = first_result['href']
            game_response = requests.get(game_url)
            if game_response.status_code == 200:
                game_html_content = game_response.text
                game_soup = BeautifulSoup(game_html_content, 'html.parser')

                game_image = game_soup.find('img', class_='game_header_image_full')
                if game_image:
                    return game_image['src']
                else:
                    print(f"Image not found for game '{game_name}'.")
            else:
                print(f"Failed to fetch game page: {game_url}")
        else:
            print(f"No results found for game '{game_name}'.")
    else:
        print(f"Failed to fetch search results for '{game_name}'. Status code: {response.status_code}")

    return None


@lru_cache(maxsize=100)
def searching_steam(game_name):
    steam = Steam(os.environ.get(""))
    user = steam.apps.search_games(game_name, country="US")
    if user is None:
        return "Game Is Not Found"
    return user


@lru_cache(maxsize=100)
def searching_epic(game_name):
    api = EpicGamesStoreAPI()
    search_results = api.fetch_store_games(keywords=game_name)

    game_results = []
    for game in search_results['data']['Catalog']['searchStore']['elements']:
        price_info = game['price']['totalPrice']
        images = game['keyImages']
        image_url = next((img['url'] for img in images if img['type'] == 'Thumbnail'),
                         images[0]['url'] if images else None)
        game_info = {
            'name': game['title'],
            'epic_price': price_info['fmtPrice']['originalPrice'],
            'discountPrice': price_info['fmtPrice']['discountPrice'],
            'img': image_url,
            "platform": "epic"
        }
        if game_name.lower() in game['title'].lower():
            game_results.append(game_info)
    return game_results


def searching_data_in_epic_and_steam(game_name):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_steam = executor.submit(searching_steam, game_name)
        future_epic = executor.submit(searching_epic, game_name)
        steam_data = future_steam.result()
        epic_data = future_epic.result()

    data = []

    if steam_data:
        for steam in steam_data['apps']:
            data.append(steam)

    if epic_data:
        for epic in epic_data:
            data.append(epic)
    return data


def fetch_image(game_name, is_steam):
    if is_steam:
        return get_game_image_from_steam(game_name)
    return None


def merge_games(games):
    merged_games = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}
        for game in games:
            name = normalize_game_name(game['name'].lower())
            print(game)
            if game['img']:
                if name not in merged_games:
                    merged_games[name] = {
                        'name': game['name'],
                        'epic_price': game.get('epic_price'),
                        'price': game.get('price'),
                        'img': game.get("img")
                    }
                    if 'id' in game:
                        futures[executor.submit(fetch_image, game['name'], True)] = name
                if name in merged_games:
                    if 'epic_price' in game:
                        merged_games[name]['epic_price'] = game['epic_price']
                    if 'price' in game:
                        merged_games[name]['price'] = game['price']
                    if 'img' not in merged_games[name] and 'img' in game:
                        merged_games[name]['img'] = game['img']

        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                img = future.result()
                if img:
                    merged_games[name]['img'] = img
            except Exception as e:
                print(f"Error fetching image: {e}")

    return list(merged_games.values())
