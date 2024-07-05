from flask import Flask, render_template, request, jsonify
from methods import searching_steam, searching_epic, searching_data_in_epic_and_steam, merge_games
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    game_name = request.json.get("game_name")
    merged_games = merge_games(searching_data_in_epic_and_steam(game_name))

    return jsonify(merged_games)


if __name__ == '__main__':
    app.run(debug=True)
