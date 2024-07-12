from epicstore_api import EpicGamesStoreAPI
import re
import concurrent.futures
from howlongtobeatpy import HowLongToBeat
import time
from .steam_api import *


def normalize_game_name(game_name):
    return re.sub(r'\W+', '', game_name.lower()) if game_name[-1] != "+" else game_name


def get_game_playtime(game_name):
    try:
        results = HowLongToBeat().search(game_name)
        if results:
            best_match = max(results, key=lambda element: element.similarity)
            return {
                    'game_name': best_match.game_name,
                    'main_story': best_match.main_story,
                    'main_extras': best_match.main_extra,
                    'completionist': best_match.completionist
                }
        else:
            print(f"No results found for game '{game_name}'")
            return None
    except requests.exceptions.ReadTimeout:
        time.sleep(3)


@lru_cache(maxsize=100)
def searching_epic(game_name, country):
    try:
        api = EpicGamesStoreAPI(locale=f'en-{country}', country=country)
        search_results = api.fetch_store_games(keywords=game_name)

        game_results = []
        for game in search_results['data']['Catalog']['searchStore']['elements']:
            if game_name.lower() in game['title'].lower():
                price_info = game['price']['totalPrice']
                current_price = price_info['fmtPrice']['discountPrice']
                initial_price = price_info['fmtPrice']['originalPrice']
                discount = price_info['discount']
                currency = price_info['currencyCode']
                images = game['keyImages']
                image_url = next((img['url'] for img in images if img['type'] == 'Thumbnail'),
                                 images[0]['url'] if images else None)
                product_slug = game.get('productSlug', '')
                game_url = f"https://www.epicgames.com/store/en-US/p/{product_slug}" if product_slug else None
                game_info = {
                    'name': game['title'],
                    'current_price': current_price,
                    'initial_price': initial_price,
                    'discount': discount,
                    'currency': currency,
                    'epic_price': price_info['fmtPrice']['originalPrice'],
                    'img': image_url,
                    "platform": "epic",
                    "description": game['description'],
                    "link": game_url
                }
                game_results.append(game_info)
        return game_results
    except Exception as err:
        print(err)


def searching_data_in_epic_and_steam(game_name, country="US"):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_steam = executor.submit(searching_steam, game_name)
        future_epic = executor.submit(searching_epic, game_name, country)
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


def get_data_from_country(game_name, country):
    data = searching_data_in_epic_and_steam(game_name, country)
    final_data = merge_games(data)
    for current_data in final_data:
        if game_name == current_data['name']:
            if current_data["price"] is not None and current_data["epic_price"] is None:
                return get_game_data(current_data['id'], country)
            elif current_data["price"] is not None and current_data["epic_price"] is not None:
                steam = get_game_data(current_data['id'], country)
                epics = searching_epic(current_data['name'], country)
                for epic in epics:
                    if game_name == current_data["name"]:
                        return {
                            'current_price_epic': epic['current_price'],
                            'initial_price_epic': epic['initial_price'],
                            'discount_epic': epic['discount'],
                            'currency_epic': epic['currency'],
                            'current_price_steam': steam['current_price'],
                            'initial_price_steam': steam['initial_price'],
                            'discount_steam': steam['discount'],
                            'currency_steam': steam['currency']
                        }
            else:
                epics = searching_epic(current_data['name'], country)
                for epic in epics:
                    if game_name == current_data["name"]:
                        return {
                            'current_price': epic['current_price'],
                            'initial_price': epic['initial_price'],
                            'discount': epic['discount'],
                            'currency': epic['currency']
                        }


def fetch_image(game_name, is_steam):
    if is_steam:
        return get_image_and_description_from_steam(game_name)["img"]
    return None


def merge_games(games):
    merged_games = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}
        for game in games:
            name = normalize_game_name(game['name'].lower())
            if game['img']:
                if name not in merged_games:
                    merged_games[name] = {
                        "id": game["id"][0] if "id" in game else None,
                        'name': game['name'],
                        'epic_price': game.get('epic_price') if "epic_price" in game else None,
                        'price': game["price"] if "price" in game else None,
                        'img': game.get("img"),
                        "details_url": f"/details/{game['name']}",
                        "steam_url": game['link'] if "id" in game else None,
                        "epic_url": game["link"] if "platform" in game else None
                    }
                    if 'id' in game:
                        futures[executor.submit(fetch_image, game['name'], True)] = name
                if name in merged_games:
                    if 'epic_price' in game:
                        merged_games[name]['epic_price'] = game['epic_price']
                    if 'price' in game:
                        merged_games[name]['price'] = game["price"]
                    if 'img' not in merged_games[name] and 'img' in game:
                        merged_games[name]['img'] = game['img']
                    if "platform" in game:
                        merged_games[name]['epic_url'] = game["link"]
                if merged_games[name]["price"] == "" and merged_games[name]["epic_price"] is None:
                    del merged_games[name]

        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                img = future.result()
                if img:
                    merged_games[name]['img'] = img
            except Exception as e:
                print(f"Error fetching image: {e}")
    return list(merged_games.values())


@lru_cache(maxsize=100)
def get_other_data(game_name):
    data = searching_data_in_epic_and_steam(game_name)
    infa = fetch_game_info(game_name)
    for current_data in data:
        if game_name == current_data['name']:
            if "id" in current_data:
                info = {
                    'img': infa["image_and_description"]["img"] if infa["image_and_description"] is not None else current_data['img'],
                    'description': infa["image_and_description"]["description"] if infa["image_and_description"] is not None else "not found",
                    "review": infa["review_summary"]['positive_percentage'] if infa["review_summary"] is not None else None,
                    "playtime": get_game_playtime(current_data["name"])['completionist'] if get_game_playtime(current_data["name"]) is not None else "Playtime not found"
                }
            else:
                info = {
                    'img': current_data['img'],
                    'description': current_data['description'],
                    "review": None,
                    "playtime": get_game_playtime(current_data["name"])['completionist'] if get_game_playtime(current_data["name"]) is not None else "Playtime not found"
                }

            return info
