import re
import glob
import nltk
import numpy as np
import pandas as pd
from pprint import pprint

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.matutils import cossim
from gensim.test.utils import datapath

import spacy
import statsmodels.api as sm

import pyLDAvis
import pyLDAvis.gensim

import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

docs = glob.glob("/data/mark/twitter/result/clean_tweets/*.csv")

frames = []
for doc in docs:
    df = pd.read_csv(doc, sep='\t')
    frames.append(df)

result = pd.concat(frames)

dates = {}
for i in range(result.shape[0]):
    date = result["created_at"].iloc[i]
    year, month, day = date.split("-")
    
    if year not in dates:
        dates[year] = {}
    
    if month not in dates[year]:
        dates[year][month] = {}
    
    if day not in dates[year][month]:
        dates[year][month][day] = 0
    
    dates[year][month][day] += 1

def train_lda(df, num_topics=20):
    df = df.dropna()
    xs = [df["cleaned_text"].iloc[i].split() for i in range(df.shape[0])]
    
    id2word = corpora.Dictionary(xs)
    texts = xs
    corpus = [id2word.doc2bow(text) for text in texts]
    
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=num_topics, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)
    return lda_model

topic_model_dates = []
topic_models = []
for i, year in enumerate(dates.keys()):
    if int(year) < 2016:
        continue

    for j, month in enumerate(dates[year].keys()):
        for k, day in enumerate(dates[year][month].keys()):
            print(i, j / len(dates[year].keys()), k / len(dates[year][month].keys()))
            date = "{}-{}-{}".format(year, month, day)

            if date in topic_model_dates:
                continue

            doc = result[result["created_at"] == date]
            model = train_lda(doc)
            
            temp_file = datapath(date)
            model.save(temp_file)
            
            topic_model_dates.append(date)
            topic_models.append(model)

def cossim_pairs(topic_models, num_topics=20):
    topic_cos_map = {}

    num_topics = 20
    for i, m in enumerate(topic_models):
        cur_date = temp_dates[i]
        month = int(cur_date.split("-")[1])
        
        if month < 9:
            break
        if month != 9:
            continue
        
        for u in range(num_topics):
            for j, n in enumerate(topic_models):
                if i == j:
                    continue
                top_cs = -1
                top_topic = ""
                for v in range(num_topics):
                    cs = cossim(m.show_topic(u), n.show_topic(v))
                    if cs > top_cs:
                        top_cs = cs
                        top_topic = "{}:{}_{}:{}".format(i, u, j, v)

                topic_cos_map[top_topic] = top_cs
    return topic_cos_map

topic_cos_map = cossim_pairs(topic_models, num_topics=20)

temp = {}
for val in sorted(topic_cos_map.items(), key=lambda kv:(-kv[1], kv[0]))[:100]:
    temp_key = val[0].split("_")[0]
    if temp_key in temp:
        continue
    temp[temp_key] = 1
    print(val[0].split("_")[0], val[1])

topic_map = {}
for key in topic_cos_map.keys():
    new_key = "{}:{}".format(key.split(":")[0], key.split(":")[1])
    value = key.split(":")[-1]
    
    topic_map[new_key] = (value, topic_cos_map[key])


lowess = sm.nonparametric.lowess

def plot_day_topic_graph(day, topic):
    ys = [topic_map["{}:{}_{}".format(day, topic, i)][1] for i in range(1, 365) if i != day][::-1]
    xs = [i for i in range(1, 364)]
    zs = lowess(ys, xs, 0.03)

    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

    tableau20 = [(c[0]/255., c[1]/255., c[2]/255.) for c in tableau20]

    plt.plot(xs, ys)
    plt.show()

    ax = plt.subplot(111)
    plt.gcf().set_size_inches(11, 5)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    plt.xticks(range(0, len(xs), 30), months)


    plt.plot(xs, ys, color=tableau20[1])
    plt.plot(zs[:, 0], zs[:, 1], color=tableau20[0])
    plt.show()

day, topic = 111, 10
plot_day_topic_graph(day, topic)

cur_model = [m for (t, m) in zip(topic_model_dates, topic_models) if int(t.split("-")[0]) == 2018][day]

def plot_date_model(lda_model, date="2018-12-25"):
    df = result[result["created_at"] == date]
    
    df = df.dropna()
    xs = [df["cleaned_text"].iloc[i].split() for i in range(df.shape[0])]
    
    id2word = corpora.Dictionary(xs)
    texts = xs
    corpus = [id2word.doc2bow(text) for text in texts]
    
    pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    
    return vis

plot_date_model(cur_model, date="2018-09-12")

