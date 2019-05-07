import csv, time, os, json
from tqdm import tqdm
import numpy as np
import pandas as pd
import json
import os
import glob
import datetime
from datetime import datetime 
from tqdm import tqdm
import pickle
from collections import OrderedDict
from collections import defaultdict
from collections import Counter
import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize  
from nltk.util import ngrams
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

stop_words = set(stopwords.words('english')) 
stopwords2 = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'us',  'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves', 'please', 'dm',"it's",'&amp;', '-', 'rt',"i'am"]
stop_words_all = list(set(stop_words) | set(stopwords2))
porter = PorterStemmer()
lancaster=LancasterStemmer()
lancaster_dic = {}
def read_all_files(num=1000):
    existing_fp = []
    file_dir = "./data/tweets_3200/"
    fashion_file = pd.read_csv('./input/fashion_name_id_6k.csv',sep='\t')
    fashion_ids = list(fashion_file['id'])[0:num]

    for i, fp in enumerate(glob.glob("./result/clean_tweets_new2/*.csv")):
        new_id = fp.split('/')[-1].split('.')[-2]
        existing_fp.append(new_id)
        # print(existing_fp)

    for i, file_id in enumerate(fashion_ids):
        if str(file_id) in existing_fp:
            print('read {}: {} already updated'.format(i,file_id))
            continue
        
        existing_fp.append(file_id)
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
        df.to_csv("./result/clean_tweets_new2/{}.csv".format(file_id), index=False, sep='\t')


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
        sen = remove_urls(sen)
        tokenizer=nltk.tokenize.RegexpTokenizer(r'\w+|@\w+|#\w+')
        sen =tokenizer.tokenize(sen) 
        hashtag_item = []
        if len(sen)!= 0 and 'RT' == sen[0]:
            if len(sen)> 1 and sen[1][0] == '@':
                sen[0] = ''
                sen[1] = ''
        cleaned_tweet, hashtag_item = get_hashtag(sen)
        cleaned_tweet = [element for element in cleaned_tweet if element != '' ]
        cleaned_tweet = ' '.join(cleaned_tweet)
        hashtags.append(hashtag_item)
        cleaned_text.append(cleaned_tweet)
    return cleaned_text, hashtags

## extract and remove hashtags,
def remove_urls(tweet):
    sen = tweet.split()
    for i, word in enumerate(sen):
        if len(word) > 20 or word[0:4] == 'http':
            sen[i] = ''
    sen = ' '.join(sen)
    return sen


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
    # remove single words
    if len(word) == 1:
        word = ''
    # remove stopwords
    if word in stop_words_all:
        word = ''
    if word != '':
        stem = lancaster.stem(word)
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
    
    if not os.path.isdir('./result/clean_tweets_new2/'):
        os.mkdir('./result/clean_tweets_new2/')
    read_all_files()
    # read_all_files()
    # read_a_file()

if __name__ == '__main__':
    main()