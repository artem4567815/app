import os
from steam_web_api import Steam
from epicstore_api import EpicGamesStoreAPI
from backend.config import steam_key
import requests
from bs4 import BeautifulSoup
import re


def normalize_game_name(game_name):
    # Удаляем все символы, кроме букв и цифр
    return re.sub(r'\W+', '', game_name.lower())



def get_game_image_from_steam(game_name):
    # Формируем URL страницы поиска Steam по названию игры
    search_url = f"https://store.steampowered.com/search/?term={game_name.replace(' ', '+')}"

    # Отправляем GET-запрос и получаем HTML-код страницы
    response = requests.get(search_url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Ищем первый результат поиска
        first_result = soup.find('a', class_='search_result_row')

        if first_result:
            # Получаем URL страницы с игрой
            game_url = first_result['href']
            game_response = requests.get(game_url)
            if game_response.status_code == 200:
                game_html_content = game_response.text
                game_soup = BeautifulSoup(game_html_content, 'html.parser')

                # Находим картинку на странице игры
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

def searching_steam(game_name):
    KEY = os.environ.get(steam_key)
    steam = Steam(KEY)
    user = steam.apps.search_games(game_name, country="US")
    if user is None:
        return "Game Is Not Found"
    return user


def searching_epic(game_name):
    api = EpicGamesStoreAPI()
    search_results = api.fetch_store_games(keywords=game_name)

    if not search_results or 'data' not in search_results or 'Catalog' not in search_results['data']:
        return {
            'originalPrice': "Game Is Not Found",
            'discountPrice': "Game Is Not Found",
            'name': "Game Is Not Found"
        }
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
        game_results.append(game_info)
    return game_results


def searching_data_in_epic_and_steam(game_name):
    epic_data = searching_epic(game_name)
    steam_data = searching_steam(game_name)
    data = []

    if steam_data:
        for steam in steam_data['apps']:
            data.append(steam)

    if epic_data:
        for epic in epic_data:
            data.append(epic)
    return data


def merge_games(games):
    merged_games = {}

    for game in games:
        name = normalize_game_name(game['name'].lower())

        if game['img']:
            if name not in merged_games:
                img = get_game_image_from_steam(game['name'])
                merged_games[name] = {
                    'name': game['name'],
                    'epic_price': game.get('epic_price'),
                    'price': game.get('price'),
                    'img': img if 'id' in game else game.get('img')
                }
            if name in merged_games:
                if 'epic_price' in game:
                    merged_games[name]['epic_price'] = game['epic_price']
                if 'price' in game:
                    merged_games[name]['price'] = game['price']
                if 'img' not in merged_games[name] and 'img' in game:
                    merged_games[name]['img'] = game['img']


    return list(merged_games.values())

