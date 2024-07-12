from flask import Flask, render_template, request, jsonify, send_from_directory
from methods import searching_data_in_epic_and_steam, merge_games, get_other_data, get_data_from_country
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
favorites_game = []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/<gameName>', methods=['POST'])
def search(gameName):
    game_name = gameName
    merged_games = merge_games(searching_data_in_epic_and_steam(game_name))

    return jsonify(merged_games)


@app.route('/search/', methods=['POST'])
def search_null():
    return jsonify([])


@app.route('/details/<game_name>', methods=['POST'])
def details_page(game_name):
    data = get_other_data(game_name)

    return jsonify(data)


@app.route('/countries', methods=['POST'])
def countries():
    countries = {
        "United States": "US",
        "Russia": "RU",
        "Great Britain": "GB",
        "Colombia": "CO",
        "Poland": "PL",
        "Germany": "DE",
        "France": "FR",
        "Spain": "ES",
        "Canada": "CA",
        "Japan": "JP",
        "Kazakhstan": "KZ",
        "Norway": "NO",
        "Korea": "KR",
        "Australia": "AU",
        "China": "CN",
        "India": "IN",
        "Brazil": "BR",
        "Turkey": "TR"
        }
    c = []
    for country in countries:
        c.append(country)

    return jsonify(c)


@app.route('/prices/<game_name>/<country>', methods=['POST'])
def price_info(game_name, country):
    countries = {
        "United States": "US",
        "Russia": "RU",
        "Great Britain": "GB",
        "Colombia": "CO",
        "Poland": "PL",
        "Germany": "DE",
        "France": "FR",
        "Spain": "ES",
        "Canada": "CA",
        "Japan": "JP",
        "Kazakhstan": "KZ",
        "Norway": "NO",
        "Korea": "KR",
        "Australia": "AU",
        "China": "CN",
        "India": "IN",
        "Brazil": "BR",
        "Turkey": "TR"
    }

    data = get_data_from_country(game_name, countries[country])
    if data is None:
        return {
            "current_price": "бесплатно",
            "initial_price": "бесплатно",
            "discount": 0,
            "currency": ""
        }
    return jsonify(data)


@app.route('/add_favorites', methods=['POST'])
def add_favorites():
    game_name = request.json.get("game_name")
    merged_games = merge_games(searching_data_in_epic_and_steam(game_name))

    for data in merged_games:
        if game_name == data['name']:
            favorites_game.append(data)
        print(favorites_game)
        return jsonify(favorites_game)


@app.route('/favorites', methods=['GET'])
def favorites():
    return jsonify(favorites_game)


if __name__ == '__main__':
    app.run(debug=True)
