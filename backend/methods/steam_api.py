import os
from steam_web_api import Steam
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from functools import lru_cache


@lru_cache(maxsize=100)
def get_steam_appid(game_name):
    try:
        url = f'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            apps = data.get('applist', {}).get('apps', [])
            for app in apps:
                if game_name.lower() == app['name'].lower():
                    return app['appid']
        return None
    except Exception as e:
        print(e)


@lru_cache(maxsize=100)
def get_image_and_description_from_steam(name):
    image_and_des_url = f"https://store.steampowered.com/search/?term={name.replace(' ', '+')}&cc=US"
    response = requests.get(image_and_des_url)
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
                game_description = game_soup.find('div', class_='game_description_snippet')
                if game_image and game_description:
                    return {
                        "img": game_image['src'],
                        "description": game_description.get_text(strip=True)
                    }
                else:
                    print(f"Image not found.")
            else:
                print(f"Failed to fetch game page: {game_url}")
        else:
            print(f"No results found.")
    else:
        print(f"Failed to fetch search results. Status code: {response.status_code}")

    return None


@lru_cache(maxsize=100)
def get_review_summary(reviews_url):
    response = requests.get(reviews_url)
    if response.status_code == 200:
        data = response.json()
        if data.get('success') == 1:
            summary = data['query_summary']
            total_reviews = summary['total_reviews']
            positive_reviews = summary['total_positive']
            if total_reviews > 0:
                positive_percentage = (positive_reviews / total_reviews) * 100
                return {
                    'total_reviews': total_reviews,
                    'positive_reviews': positive_reviews,
                    'negative_reviews': total_reviews - positive_reviews,
                    'positive_percentage': positive_percentage
                }
            else:
                print(f"No reviews found for app_id.")
        else:
            print(f"Failed to fetch reviews for app_id.")
    else:
        print(f"Failed to fetch data from Steam API. Status code: {response.status_code}")
    return None


@lru_cache(maxsize=100)
def get_game_data(app_id, country):
    price_url = f'https://store.steampowered.com/api/appdetails?appids={app_id}&cc={country}'
    response = requests.get(price_url)
    if response.status_code == 200:
        data = response.json()
        if str(app_id) in data and data[str(app_id)]['success']:
            if "price_overview" in data[str(app_id)]['data']:
                game_info = data[str(app_id)]['data']['price_overview']
                print(game_info['initial_formatted'], "-------")
                return {
                    "current_price": game_info['final_formatted'],
                    "initial_price": game_info['initial_formatted'],
                    "discount": game_info['discount_percent'],
                    "currency": game_info['currency']
                }
            else:
                return None
    return None


@lru_cache(maxsize=100)
def searching_steam(game_name):
    try:
        steam = Steam(os.environ.get(""))
        user = steam.apps.search_games(game_name)
        if user is None:
            return "Game Is Not Found"
        return user
    except Exception as e:
        print(e)


@lru_cache(maxsize=100)
def fetch_game_info(app_name):
    app_id = get_steam_appid(app_name)

    reviews_url = f"https://store.steampowered.com/appreviews/{app_id}?json=1"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_image_and_description = executor.submit(get_image_and_description_from_steam, app_name)
        future_review_summary = executor.submit(get_review_summary, reviews_url)

        image_and_description = future_image_and_description.result()
        review_summary = future_review_summary.result()

    return {
        "image_and_description": image_and_description,
        "review_summary": review_summary,
    }
