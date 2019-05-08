import json
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
    file_name = "./files/{}/{}_totalcounts_{}.csv".format(time_frame ,word_type,time_frame)
    print(file_name)
    hashtags = utils.csv_reader(file_name)

    res = {
        "data": hashtags
    }
    # print(word_type,time_frame)
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

    dates_file = utils.read_csv("bucketsperdate.csv")
    hashtags = list(dates_file.loc[dates_file["date"] == date, "hashtag"])[0]

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
        form: [hashtags, unigrams],
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

    path = "./files/{}/{}_{}.pkl".format(year, form, year)

    utils.get_plot(path, value)

    return jsonify({}), 201

@app.route("/")
def index():
    return jsonify("Backend running")


if __name__ == "__main__":
    app.run(debug=True, port=5000)

