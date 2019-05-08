import operator
import csv
import pylab

import numpy as np
import pandas as pd
import datetime as dt
import matplotlib 
import matplotlib.pyplot as plt

matplotlib.use('Agg')

def csv_reader(filename):
    """
    Sends the top 50 total counts file per year
    """
    reader = csv.reader(open(filename))  
    result = {}
    for row in reader:
        key = row[0]
        result[key] = int(row[1])
    sorted_result = sorted(result.items(), key=operator.itemgetter(1))
    sorted_result = sorted_result[::-1]

    return (sorted_result[:50])

def read_csv(filename):
    df = pd.read_csv(filename)

    return df

def get_plot(path, value):
    data = pd.read_pickle(path)

    x_ticks = list(data.columns)
    x_ticks_dates = [str(d).split(" ")[0] for d in x_ticks]

    y= np.array(data.loc[value,:])
    lag = 15
    threshold = 4
    influence = 0.5
    result = thresholding_algo(y, lag=lag, threshold=threshold, influence=influence)
    
    create_plot(value, x_ticks_dates,y,result)

def create_plot(value, x_ticks_dates,y,result):
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
    
    dates = {}
    for i in range(len(x_ticks_dates)):
        year, month, day = x_ticks_dates[i].split("-")

        if year not in dates:
            dates[year] = {}

        if month in dates[year]:
            x_ticks_dates[i] = ""
        else:
            x_ticks_dates[i] = "{}, {}".format(month, year)
            dates[year][month] = 1
    
    plt.subplot(212)
    plt.step(x_ticks_dates, result["signals"], color="red", lw=2)
    plt.ylim(-1.5, 1.5)
    plt.gcf().autofmt_xdate()
    #plt.savefig(value + '.png')
    plt.savefig("../frontend/public/fash.png")
    plt.close()
    return 

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


if __name__ == "__main__":
    pass

