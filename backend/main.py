import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

import utils

app = Flask(__name__)
CORS(app)

@app.route("/hashtags", methods=['GET'])
def get_hashtags():
    """
    Get all of the available hashtags
    """
    hashtags = utils.csv_reader("hashtag_counts.csv")

    res = {
        "data": hashtags
    }

    return jsonify(res), 201

@app.route("/dates", methods=['GET'])
def get_dates()
    """
    Get all of the available dates
    """
    dates_file = utils.csv_reader("bucketsperdate.csv")
    dates = list(dates_file)["date"]

@app.route("/hashtags_date", methods=['POST'])
def get_hashtags_date():
    """
    Get all of the available hashtags for a certain day
    """
    dates_file = utils.csv_reader("bucketsperdate.csv")
    dates = list(dates_file)["date"]

@app.route("/plots", methods=['POST'])
def post_plots():
    """
    Create a plot of the spike

    request = {
      year: [2016, 2017, 2018, 2019],
      form: [hashtag, unigram],
      value: "#fash"
    }
    """
    data = json.loads(request.data)

    # if there is an error in the request
    if "year" not in data or "form" not in data or "value" not in data:
        return jsonify({}), 400

    year = data["year"]
    form = data["form"]
    value = data["value"]

    return jsonify({}), 201

@app.route("/")
def index():
    return jsonify("Backend running")


if __name__ == "__main__":
    app.run(debug=True, port=5000)

