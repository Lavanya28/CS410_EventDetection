import csv
import operator
import numpy as np
import pylab
import pandas as pd
import datetime as dt
import matplotlib 
import matplotlib.pyplot as plt

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

matplotlib.use('Agg')
app = Flask(__name__)
CORS(app)

#send the total counts file per year to fetch top 50
def csv_reader(filename):
    reader = csv.reader(open(filename))  
    result = {}
    for row in reader:
        key = row[0]
        result[key] = int(row[1])
    sorted_result = sorted(result.items(), key=operator.itemgetter(1))
    sorted_result = sorted_result[::-1]

    return (sorted_result[0:50])

def thresholding_algo(y, lag, threshold, influence):
    signals = np.zeros(len(y))
    filteredY = np.array(y)
    avgFilter = [0]*len(y)
    stdFilter = [0]*len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
            if y[i] > avgFilter[i-1] and avgFilter[i-1]!=0 and y[i]>3:
                signals[i] = 1   
            else:
                signals[i] = 0

            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])
        else:
            signals[i] = 0
            filteredY[i] = y[i]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])

    return dict(signals = np.asarray(signals),
                avgFilter = np.asarray(avgFilter),
                stdFilter = np.asarray(stdFilter))

#gets called by check_datapoint to plot for a particular hashtag/word and uear the distribution
def plotter(value, x_ticks_dates,y,result):
    
    threshold = 4
    
    plt.subplot(211)

    plt.plot(x_ticks_dates, y)
    plt.plot(x_ticks_dates,
               result["avgFilter"], color="cyan", lw=2)
    plt.plot(x_ticks_dates,
               result["avgFilter"] + threshold * result["stdFilter"], color="green", lw=2)
    plt.plot(x_ticks_dates,
               result["avgFilter"] - threshold * result["stdFilter"], color="green", lw=2)
    plt.gcf().autofmt_xdate()
    
    
    plt.subplot(212)
    plt.step(x_ticks_dates, result["signals"], color="red", lw=2)
    plt.ylim(-1.5, 1.5)
    plt.gcf().autofmt_xdate()
    plt.savefig(value + '.png')
    plt.close()
    return 

# send date, value = hastag/words , tag indicicating hastag/unigram/word pairs
def check_datapoint(date='2016', value="#fash", tag="hashtag"):

    if(tag=="hashtag"):
        if(date=="2016"):
            #update pickle files of dates here 
            #data = pd.read_pickle('hashtags_matrix_2016.pkl')
            data = pd.read_pickle('./files/2016/hashtags_2016.pkl')
            x_ticks = list(data.columns)
            print(x_ticks)
            """
            x_ticks_dates = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in x_ticks]
            y= np.array(data.loc[value,:])
            lag = 15
            threshold = 4
            influence = 0.5
            result = thresholding_algo(y, lag=lag, threshold=threshold, influence=influence)
            
            
            plotter(value, x_ticks_dates,y,result)
            """
            
            
            return
    # write more date conditions here 

@app.route("/hashtags", methods=['GET'])
def get_hashtags():
    hashtags = csv_reader("hashtag_counts.csv")

    res = {
        "data": hashtags
    }

    return jsonify(res), 201

@app.route("/", methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        if request.form['top'] == 'Top trending Hastags':
            result = csv_reader('hashtag_counts.csv')
            check_datapoint()
            return render_template("home.html", result=result)
                
        elif request.form['top'] == 'Top trending Words':

            return render_template("home.html")


        elif request.form['top'] == 'Top trending Word-pairs':

            return render_template("home.html")

        else:
            pass
            
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

