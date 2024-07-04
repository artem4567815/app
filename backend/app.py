from flask import Flask, render_template, request, jsonify
from methods import searching_steam, searching_epic
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    game_name = request.json.get('game_name')
    game_data = searching_steam(game_name)
    epic_data = searching_epic(game_name)
    apps = []

    if not game_data["apps"]:
        test_data = [
            {
                "name": epic_data['name'],
                "steam_price": "Game is not found",
                "epic_price": '$' + epic_data["originalPrice"],
                "img": epic_data['img'],
                "details_url": f"/details/{None}"
            }
        ]
        if test_data[0]['name'] != "Game Is Not Found":
            apps.append(test_data)
    for game in game_data["apps"]:
        print(game)
        test_data = [
            {
                "name": game["name"],
                "steam_price": game["price"],
                "epic_price": epic_data['originalPrice'] if epic_data['name'].lower() == game['name'].lower() else "Game is not found",
                "img": game['img'],
                "details_url": f"/details/{None}"
            }
        ]
        apps.append(test_data)
        if game['name'] != game_name:
            test_data = [
                {
                    "name": epic_data['name'],
                    "steam_price": "Game is not found",
                    "epic_price": '$' + epic_data["originalPrice"],
                    "img": epic_data['img'],
                    "details_url": f"/details/{None}"
                }
            ]
            if test_data[0]['name'] != "Game Is Not Found":
                apps.append(test_data)
    return jsonify(apps)


if __name__ == '__main__':
    app.run(debug=True)
