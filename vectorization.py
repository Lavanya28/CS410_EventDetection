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
from tqdm import tqdm
import glob

def read_all_files_hashtags():
    for i, file in enumerate(glob.glob("./result/clean_tweets/*.csv")):
        # if i > 1:
        #     break
        file_id = file.split('/')[-1]
        print('read {}: {}'.format(i,file_id)) 
        node_file = pd.read_csv(file, sep = '\t')
        dates = list(node_file['created_at'])
        new_file = node_file.loc[node_file["hashtags"] != "[]",['created_at', 'hashtags']]
        dates = list(new_file['created_at'])
        hashtags = list(new_file['hashtags'].tolist())
        dates_dic = get_dates_dict(dates, hashtags, True)
        with open('./result/hashtags/{}.json'.format(file_id), 'w') as fp:
            json.dump(dates_dic, fp, sort_keys=True, indent= 2)


def read_all_files():
    for i, file in enumerate(glob.glob("./result/clean_tweets/*.csv")):
        # if i > 1:
        #     break
        file_id = file.split('/')[-1]
        print('read {}: {}'.format(i,file_id)) 
        node_file = pd.read_csv(file, sep = '\t')
        dates = list(node_file['created_at'])
        clean_text = list(node_file['cleaned_text'])
        dates_dic = get_dates_dict(dates, clean_text)
        with open('./result/BOWS/{}.json'.format(file_id), 'w') as fp:
            json.dump(dates_dic, fp, sort_keys=True, indent= 2)

        df = pd.DataFrame({'dates': list(dates_dic.keys())})
        df.to_csv("./result/dates", index=False, sep='\t')

def get_dates_dict(dates, clean_text, is_hashtag=False):
    dates_dic = {}
    for i, date in enumerate(dates):
        if not clean_text[i] or pd.isna(clean_text[i]):
            continue
        if is_hashtag:
            new_text_counter = get_hashtag_counter(clean_text[i])
        else:
            new_text_counter = get_bow_counter(clean_text[i])
        # print("new_text_counter", new_text_counter)
        if date not in dates_dic.keys():
            dates_dic[date] = dict(new_text_counter)
        else:
            dates_dic[date] = sum_counter(Counter(dates_dic[date]),new_text_counter)
    return dates_dic

def get_hashtag_counter(hashtags):
    text = hashtags[1:-1]
    sen = text.split(', ')
    sen = [hashtag[1:-1] for hashtag in sen]
    sen_counter = Counter(sen)
    # print(sen_counter)
    return sen_counter


def get_bow_counter(text):
    sen = text.split(' ');
    sen_counter = Counter(sen)
    return sen_counter


def sum_counter(A,B):
    return sum((A, B), Counter())


def read_all_dicts():
    hashtags_dicts = {}
    for i, file in enumerate(glob.glob("./result/hashtags/*.json")):
        file_id = file.split('/')[-1]
        print('read {}: {}'.format(i,file_id)) 
        # if i > 1: 
        #     break
        with open(file) as f:
            data = json.load(f)
            # print(data)
        hashtags_dicts = sum_two_nested_counter(hashtags_dicts,data)
    with open('./result/hashtag_volumes.json', 'w') as fp:
        json.dump(hashtags_dicts, fp, sort_keys=True, indent= 2)
    # print(hashtags_dicts)
# def merge_all_dicts(A,B):
def sum_two_nested_counter(A,B):
    counts = defaultdict(Counter)
    for k, d in A.items():
        counts[k].update(d)
    for k, d in B.items():
        counts[k].update(d)
    return counts
    # print(counts)

def main():
    if not os.path.isdir('./result/BOWS/'):
        os.mkdir('./result/BOWS/')
    # read_all_files()
    # read_all_files_hashtags()
    # read_all_files()
    # read_a_file()
    read_all_dicts()

if __name__ == '__main__':
    main()