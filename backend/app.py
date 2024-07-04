from flask import Flask, render_template, request, jsonify
#from models import db, Game
#import config
from methods import searching
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
#db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    game_name = request.json.get('game_name')
    game_data = searching(game_name)
    apps = []
    print(game_data["apps"])
    for game in game_data["apps"]:
        test_data = [
            {
                "name": game["name"],
                "steam_price": game["price"],
                "epic_price": None,
                "details_url": f"/details/{None}"
            }
        ]
        apps.append(test_data)
    return jsonify(apps)


if __name__ == '__main__':
    app.run(debug=True)
