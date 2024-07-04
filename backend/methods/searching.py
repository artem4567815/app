import os
from steam_web_api import Steam
from epicstore_api import EpicGamesStoreAPI
from backend import steam_key

def searching_steam(game_name):
    KEY = os.environ.get(steam_key)
    steam = Steam(KEY)
    user = steam.apps.search_games(game_name)
    if user is None:
        return "Game Is Not Found"
    return user


def searching_epic(game_name):
    api = EpicGamesStoreAPI()
    search_results = api.fetch_store_games(keywords=game_name)

    # Проверка на наличие данных
    if not search_results or 'data' not in search_results or 'Catalog' not in search_results['data']:
        return None

    for game in search_results['data']['Catalog']['searchStore']['elements']:
        if game['title'].lower() == game_name.lower():
            price_info = game['price']['totalPrice']
            images = game['keyImages']
            image_url = next((img['url'] for img in images if img['type'] == 'Thumbnail'),
                             images[0]['url'] if images else None)
            return {
                'originalPrice': price_info['fmtPrice']['originalPrice'],
                'discountPrice': price_info['fmtPrice']['discountPrice'],
                'name': game['title'],
                "img": image_url
            }

    return {
                'originalPrice': "Game Is Not Found",
                'discountPrice': "Game Is Not Found",
                'name': "Game Is Not Found"
            }


# Пример использования функции
price = searching_epic("War Of Tanks")
if price:
    print(f"Original Price: {price['originalPrice']}, Discount Price: {price['discountPrice']}")
else:
    print("Game not found or no price information available.")

