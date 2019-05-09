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
        result[key] = int(float(row[1]))
    sorted_result = sorted(result.items(), key=operator.itemgetter(1))
    sorted_result = sorted_result[::-1]

    return (sorted_result[:50])

def read_csv(filename):
    df = pd.read_csv(filename)

    return df

def get_plot(path, value, title):
    data = pd.read_pickle(path)

    x_ticks = list(data.columns)
    x_ticks_dates = [str(d).split(" ")[0] for d in x_ticks]

    y= np.array(data.loc[value,:])
    lag = 15
    threshold = 4
    influence = 0.5
    result = thresholding_algo(y, lag=lag, threshold=threshold, influence=influence)
    
    return create_plot(value, x_ticks_dates, y, result, title)

def create_plot(value, x_ticks_dates, y, result, title):
    threshold = 4

    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

    tableau20 = [(c[0]/255., c[1]/255., c[2]/255.) for c in tableau20]

    ax = plt.subplot(111)
    plt.gcf().set_size_inches(11, 5)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    plt.plot(x_ticks_dates, y, color=tableau20[1])
    plt.plot(x_ticks_dates,
               result["avgFilter"], color=tableau20[0], lw=2)
    plt.step(x_ticks_dates, result["signals"] * np.max(y), color=tableau20[2], lw=2)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    plt.xticks(range(0, len(x_ticks_dates), 30), months)

    fig_path = "../frontend/public/{}.png".format(title)

    plt.savefig(fig_path, bbox_inches="tight")
    plt.close()

    return fig_path

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

