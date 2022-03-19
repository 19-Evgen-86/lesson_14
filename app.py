import json

from flask import Flask, jsonify
import utils as db

app = Flask(__name__)


@app.route('/movie/<title>', methods=['GET'])
def get_film_by_title(title):
    response = db.search_by_title(title)
    return jsonify(response)


@app.route('/movie/<int:start>/to/<int:end>', methods=['GET'])
def get_film_by_year_to_year(start, end):
    response = db.search_year_to_year(start, end)
    return jsonify(response)


@app.route('/rating/<rating>', methods=['GET'])
def get_film_by_taring(rating):
    response = db.search_by_rating(rating)
    return jsonify(response)


@app.route('/genre/<genre>', methods=['GET'])
def get_film_by_genre(genre):
    response = db.search_by_genre(genre)
    return jsonify(response)


if __name__ == '__main__':
    app.run()
