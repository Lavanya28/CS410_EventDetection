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

from enum import Enum
class Type(Enum):
    hashtag = 1
    unigram = 2
    word_pair = 3

def read_all_files_hashtags():
    for i, file in enumerate(glob.glob("./result/clean_tweets_updated/*.csv")):
        file_id = fp.split('/')[-1].split('.')[-2]
        print('read {}: {}'.format(i,file_id)) 
        node_file = pd.read_csv(file, sep = '\t')
        dates = list(node_file['created_at'])
        new_file = node_file.loc[node_file["hashtags"] != "[]",['created_at', 'hashtags']]
        dates = list(new_file['created_at'])
        hashtags = list(new_file['hashtags'].tolist())
        dates_dic = get_dates_dict(dates, hashtags, Type.hashtag)
        with open('./result/hashtags/{}.json'.format(file_id), 'w') as fp:
            json.dump(dates_dic, fp, sort_keys=True, indent= 2)


def read_all_files_BOW():
    for i, file in enumerate(glob.glob("./result/clean_tweets_updated/*.csv")):
        file_id = fp.split('/')[-1].split('.')[-2]
        print('read {}: {}'.format(i,file_id)) 
        node_file = pd.read_csv(file, sep = '\t')
        dates = list(node_file['created_at'])
        clean_text = list(node_file['cleaned_text'])
        dates_dic = get_dates_dict(dates, clean_text, Type.unigram)
        with open('./result/BOWS/{}.json'.format(file_id), 'w') as fp:
            json.dump(dates_dic, fp, sort_keys=True, indent= 2)

        df = pd.DataFrame({'dates': list(dates_dic.keys())})
        df.to_csv("./result/dates", index=False, sep='\t')

def word_pairs():
    for i, file in enumerate(glob.glob("./result/clean_tweets_updated/*.csv")):
        # if i > 1:
        #     break
        file_id = file.split('/')[-1].split('.')[-2]
        print('read {}: {}'.format(i,file_id)) 
        # print(file_id)
        node_file = pd.read_csv(file, sep = '\t')
        dates = list(node_file['created_at'])
        clean_text = list(node_file['cleaned_text'])
        dates_dic = get_dates_dict(dates, clean_text, Type.word_pair)
        with open('./result/word_pairs/{}.json'.format(file_id), 'w') as fp:
            json.dump(dates_dic, fp, sort_keys=True, indent= 2)

def get_word_pair_dict(dates, clean_text):
    dates_dic = {}
    for i, date in enumerate(dates):
        if not clean_text[i] or pd.isna(clean_text[i]):
            continue
        new_text_counter = get_word_pair_counter(clean_text[i])
        print(new_text_counter)


def get_dates_dict(dates, clean_text, type):
    # print(type.value == 3)
    dates_dic = {}
    new_text_counter = None 
    for i, date in enumerate(dates):
        if not clean_text[i] or pd.isna(clean_text[i]):
            continue
        if type.value == 1:  
            new_text_counter = get_hashtag_counter(clean_text[i])
        elif type.value == 2:
            new_text_counter = get_bow_counter(clean_text[i])
        elif type.value == 3:
            new_text_counter = get_word_pair_counter(clean_text[i])

        # print("new_text_counter", new_text_counter)
        if new_text_counter != None:
            if date not in dates_dic.keys():
                dates_dic[date] = dict(new_text_counter)
            else:
                dates_dic[date] = sum_counter(Counter(dates_dic[date]),new_text_counter)
    return dates_dic

def get_word_pair_counter(text):
    items = text.split()
    new_list = ["_".join([items[i],items[j]]) for i in range(len(items)) for j in range(i+1, len(items))]
    list_counter = Counter(new_list)
    return list_counter

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


def read_all_dicts(type):
    read_file = ''
    write_file = ''
    if type.value == 1:
        read_file = "./result/hashtags/*.json"
        write_file = './result/hashtag_volumes.json'
    elif type.value == 2:
        read_file = "./result/BOWS/*.json"
        write_file = './result/unigram_volumes.json'
    elif type.value == 3:
        read_file = "./result/word_pairs/*.json"
        write_file = './result/word_pair_volumes.json'

    hashtags_dicts = {}
    for i, file in enumerate(glob.glob(read_file)):
        file_id = file.split('/')[-1]
        print('read {}: {}'.format(i,file_id)) 
        with open(file) as f:
            data = json.load(f)
        hashtags_dicts = sum_two_nested_counter(hashtags_dicts,data)
    with open(write_file, 'w') as fp:
        json.dump(hashtags_dicts, fp, sort_keys=True, indent= 2)

def sum_two_nested_counter(A,B):
    counts = defaultdict(Counter)
    for k, d in A.items():
        counts[k].update(d)
    for k, d in B.items():
        counts[k].update(d)
    return counts

def main():

    if not os.path.isdir('./result/word_pairs/'):
        os.mkdir('./result/word_pairs/')
    # read_all_files_BOW()
    # read_all_files()
    # read_all_files_hashtags()
    # read_all_files()
    # read_a_file()
    read_all_dicts(Type.word_pair)
    # word_pairs()

if __name__ == '__main__':
    main()