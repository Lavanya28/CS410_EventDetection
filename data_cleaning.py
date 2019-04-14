import csv, time, os, json
from tqdm import tqdm
import numpy as np
import pandas as pd
import json
import os
import datetime
from datetime import timedelta
from tqdm import tqdm
import pickle
from collections import OrderedDict
from collections import defaultdict
import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize  
from nltk.util import ngrams
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

punctuations = ['…',',','.','!','?','/','~','|','"', '+',':', '(', ')', '*','-']
stop_words = set(stopwords.words('english')) 

def read_all_files(num=1000):
	fashion_file = pd.read_csv('./input/fashion_name_id_6k.csv',sep='\t')
	# screen_names = list(fashion_file['screen_name'])
	fashion_ids = list(fashion_file['id'])[0:1000]
	print(fashion_ids)

def main():
	read_all_files()
    # if not os.path.isdir('./data/vogue_list_tweets_analysis'):
    #     os.mkdir('./data/vogue_list_tweets_analysis')
    # read_all_files()
    # read_a_file()

if __name__ == '__main__':
    main()