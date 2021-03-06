import json
import numpy as np
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

import utils

app = Flask(__name__)
CORS(app)

@app.route("/get_spike_detection", methods=['POST'])
def get_spike_detection():
    """
    Get all of the available hashtags
    """
    word_type = request.get_json()["word_type"]
    time_frame = request.get_json()["time_frame"]

    file_name = "./files/{}/{}_totalcounts_{}.csv".format(time_frame, word_type, time_frame)
    # print(file_name)

    data = utils.csv_reader(file_name)

    res = {
        "data": data
    }
    return jsonify(res), 201

@app.route("/dates", methods=['GET'])
def get_dates():
    """
    Get all of the available dates
    """
    dates_file = utils.read_csv("bucketsperdate.csv")
    dates = list(dates_file["date"])

    res = {
        "data": dates
    }

    return jsonify(res), 201

@app.route("/hashtags_date", methods=['POST'])
def post_hashtags_date():
    """
    Get all of the available hashtags for a certain day

    request = {
        date
    }
    """
    data = json.loads(request.data)

    if "date" not in data:
        return jsonify({}), 400

    date = data["date"]
    day, month, year = date.split("/")
    day = int(day)
    month = int(month)
    year = year[2:]
    date = "/".join([str(day), str(month), str(year)])

    dates_file = utils.read_csv("bucketsperdate.csv")
    hashtags = dates_file.loc[dates_file["date"] == date]["hashtag"].iloc[0]
    hashtags = [x[1:-1] for x in hashtags[1:-1].split(", ")]

    res = {
        "data": hashtags
    }

    return jsonify(res), 201

@app.route("/plots", methods=['POST'])
def post_plots():
    """
    Create a plot of the spike

    request = {
        year: [2016, 2017, 2018, 2019],
        form: [hashtags, unigrams, wordpairs],
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

    if form == "wordpairs":
        form = "wordpair"

    path = "./files/{}/{}_{}.pkl".format(year, form, year)

    title = value
    if form == "hashtags":
        title = title[1:]

    fig_path = utils.get_plot(path, value, title)
    fig_path = fig_path.split("/")[-1]

    if form == "hashtags":
        title = "#" + title

    res = {
        "path": fig_path,
        "title": title
    }

    print(res)

    return jsonify(res), 201

@app.route("/")
def index():
    return jsonify("Backend running")


if __name__ == "__main__":
    app.run(debug=True, port=5000)

