import csv, time, os, json
from tqdm import tqdm
import numpy as np
import pandas as pd
import json
import os
import datetime
from datetime import datetime 
from tqdm import tqdm
import pickle
from collections import OrderedDict
from collections import defaultdict
import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize  
from nltk.util import ngrams
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

punctuations = ['…',',','.','!','?','/','~','|','"', '+',':', '(', ')', '*','-']
stop_words = set(stopwords.words('english')) 
porter = PorterStemmer()
lancaster=LancasterStemmer()
lancaster_dic = {}
def read_all_files(num=1000):
    file_dir = "./data/tweets_3200/"
    fashion_file = pd.read_csv('./input/fashion_name_id_6k.csv',sep='\t')
    fashion_ids = list(fashion_file['id'])[0:num]
    for i, file_id in enumerate(fashion_ids):
        print('read {}: {}'.format(i,file_id)) 
        file = file_dir + str(file_id) + '.csv'
        node_file = pd.read_csv(file, sep = ',')
        tweets = list(node_file['text'])
        cleaned_tweets, hashtags = clean_tweets(tweets)
        new_dates = clean_dates(list(node_file['created_at']))
        df = pd.DataFrame({'id': list(node_file['id']),
                           'created_at': new_dates,
                           'hashtags':hashtags,
                           'cleaned_text': cleaned_tweets,
                           # 'original_test':tweets
                           })
        df.to_csv("./result/clean_tweets/{}.csv".format(file_id), index=False, sep='\t')

def clean_dates(dates):
    new_dates = []
    for date in dates:
        date = datetime.strptime(date.split(' ')[0], '%Y-%m-%d').strftime('%Y-%m-%d')
        new_dates.append(date)
    return new_dates 
def clean_tweets(tweets):
    tweets = tweets
    cleaned_text = []
    hashtags = []
    for i, sen in enumerate(tweets):
        # print(sen)
        sen = sen.split()
        hashtag_item = []
        if 'RT' == sen[0]:
            if sen[1][0] == '@':
                sen[0] = ''
                sen[1] = ''
        cleaned_tweet, hashtag_item = get_hashtag(sen)
        cleaned_tweet = [element for element in cleaned_tweet if element != '' ]
        cleaned_tweet = ' '.join(cleaned_tweet)
        hashtags.append(hashtag_item)
        cleaned_text.append(cleaned_tweet)
    return cleaned_text, hashtags

## extract and remove hashtags, 
def get_hashtag(tweet):
    hashtags = []
    for i,word in enumerate(tweet):
        temp_list = word.split('#')
        if len(temp_list) > 1:
            has = True
            if temp_list[0] != '':
                tweet[i] = temp_list[0]
            else:
                tweet[i] = ''
            temp_list = temp_list[1:]
            for hashtag in temp_list:                    
                hashtag = word_preprocess(hashtag)
                if hashtag != '': 
                    hashtag =  '#' + hashtag.lower()
                    if hashtag not in hashtags:
                        hashtags.append(hashtag)
        else:
            tweet[i] = word_preprocess(word)
    return tweet, hashtags

## remove urls, stopwords, punctuations, 
## lemmatize and stem each word
def word_preprocess(word):
    word = word.lower()
    word = word.encode("ascii", errors="replace").decode()
    if len(word) == 1 or (len(word) > 20 or word[0:4] == 'http'):
        word = ''
    for punct in punctuations:
        word_list = [x for x in word.split(punct) if x]
        if len(word_list) > 0:
            word = word_list[0]
        else:
            word = ''
    if word in stop_words:
        word = ''
    if word != '':
        stem = lancaster.stem(word)
        # add_lancaster_dic(stem, word)
        word = stem
    return word

def add_lancaster_dic(stem, word):
    if stem in lancaster_dic.keys():
            if word not in lancaster_dic[stem]:
                lancaster_dic[stem].append(word)
    else:
        lancaster_dic[stem] = [word]
    print(lancaster_dic)   
def main():
    
    if not os.path.isdir('./result/clean_tweets/'):
        os.mkdir('./result/clean_tweets/')
    read_all_files()
    # read_all_files()
    # read_a_file()

if __name__ == '__main__':
    main()