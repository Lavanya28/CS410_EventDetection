# CS410_EventDetection

##  Documentation of the usage of the software

### Requirements

- python 3.7.2
- node
- npm

### Running the web interface
- cd ```./backend```
  - unzip ```./backend/files.zip```
  - run the backend: ```python3 main.py```
- cd ```./frontend```
  - ```npm install```
  - ```npm start```

## Approaches
### 1. Data preprocessing 
```python3 ./data_cleaning.py``` 
In this section we implement cleaning of the twitter data scraped from 1000 different fashion accounts each consisting of 3200 tweets (Twitter API can only crawl the most 3200 tweets for each account). We also want to remove some of the extra text that usually   retweets.  For example, we remove the “RT” that appears before the text as well as the screen name of the user that is being retweeted
In addition to cleaning the data, we separate the hashtags from the main text of the tweet. 
After removing the hashtags, we remove the non-ascii characters in the text such as emojis
We also remove single characters, punctuations, and the stopword.  Since the stopwords provided by nltk is not comprehensive, we also add some of our own extra stop words.After cleaning the text, we use the lancaster stemmer to stem each of the words. 
At the end, we save the cleaned text into other csv files. This includes removal of urls, hashtags, stopwords, punctuations and emoticons. Following which we implement stemming and lemmetization on the cleaned tweets.  

The code located at ```./data_cleaning.py``` contains the functions that implement each of the removal and cleaning step.

The code is structured as follows: 
- ```clean_dates``` in the original file, we have the date and time of the tweet. Since we only care about the date, we did this preprocessing step to remove the time.
- ```clean_tweets```: 
  - nltk.tokenize.RegexpTokenizer(r'\w+|@\w+|#\w+')``` (remove punctuation and non @ symbols)
- ```get_hastags```: extract hashtags and remove from the text 
- ```remove_urls```: remove urls
- ```word_preprocess```: 
  - remove non English words,non-ascii characters,stopwords(for the stopwords, in addition to NLTK stopwords, we also created a more comprehensive stop word list) ```
  - lancasting and stemming 

The code generates a csv file inside ```.\clean_tweets\``` for each account, in the csv it contains 
  - clean date for each tweet
  - clean text for each tweet
  - extracted hashtags for each tweet


### 2. Vectorization
In this section, we implemented the vectorization of on the cleaned data. 
- First, it will count
  - ```get_hashtag_counter``` hastags based on date for each account
  - ```get_bow_counter``` BOWs based on date for each account
  - ```get_word_pair_counter```word pair (every combination of words in the tweet) for each account.
  - The data are generated inside:
	  -  ```./results/BOWS/```
	  -  ```./results/hashtags/```
	  - ```./results/word_pairs/```
- Second, it will do a time series combination:
  - ```sum_two_nested_counter```: merge all the counts for hastags, BOWS and word pairs of all 1000 accounts into a JSON format sorted by the date. This create volumes of hastags, BOWS and word pairs of top 1000 accounts in times series order.
  -The data are generated inside:
	  -  ```./results/hashtags_volumes.json/```
	  -  ```./results/unigram_volumes.json/```
	  ```./results/word_pair_volumes.json/```


### 3. Spike Detection:
Since we are only able to get the past 3200 tweets, we may not get older tweets for all of the 1000 users.  Thus, we will try to concentrate on only looking at the spikes for spike detection in the more recent years.

Our dataset in general poses two main challenges that make it difficult to detect spikes in the data. A global average would have a lot of noise and peaks computed based on this average would spike at points with no significant meaning. To address this issue, a dynamic value must be computed to allow detection of spikes in real-time. The algorithm we use is built on the 'smoothed z-score algorithm'; it takes in 3 input values, the lag, threshold and the influence. It constructs a moving mean and verifies if a data point is a certain number of standard deviation points away from the moving mean, this number of standard deviation is determined by the threshold variable. If it's a certain number of standard deviations away, we consider the data-point to be a spike. To determine how many data-points compute the moving mean, we use the lag variable. The influence decides how much impact the previous spike signal has on the detection at the current data-point. This algorithm proves to be very robust for our use case, as it constructs moving means and standard deviations that is capable of detecting spike values in the time-series for noisy twitter data. 
This concept was extended to both unigrams and word-pairs. To improve our results and provide better insight to users about the events trending on a particular day, we take the count of spikes on a per-day basis and provide users with the ability to filter based on individual dates. 

The code is structured as follows: 
- ```./backend/main.py```: contains the backend code to render our algorithms on our dataset files
- csv_reader: Outputs the top 50 trend based on the file fed as input 
- thresholding_algo: Computes the array for spikes, average running mean and the standard deviation, to decide if a data-point is a spike or not we use the formula check for the following two conditions data[i] - moving_average[i-1] > threshold * stdDeviation[i-1] and moving_average[i-1]!=0 and data[i]>(a certain integer based on hashtag/unigram/word). 
- plotter: Generates graphs for all the data including spikes


### 4. Event Detection:  
To gain better insight into the data, we aggregate the counts of spikes on a per-date basis. This would give users the ability to view trending events on a particular date. For example, if the users picks the date 19th May 2018, he would be able to view hastags and words that correlate with the royal wedding.  

### 5. Topic Modeling: 
An alternative method for doing event detection is through the use of topic models as presented in Using Topic Modeling and Similarity Thresholds to Detect Events by Keane et al.  To do this, for every day (D days) in our dataset, we create a topic model with K topics (20 in our case).  We then take the cosine similarity for each topic in each day with every other topic in other days.  For every topic we do this, we only keep the topic corresponding to the highest cosine similarity.  After this is computed, we will have a DxKx(D-1)x(K-1) values.  We can take the cosine similarities corresponding to each day to get a graph where a large enough peak means that there is an event.  We use lowess smoothing to smooth out the graph to see the events for every topic.

The code is in
- ./backend/topic_models.py: For the topic model code in a python file
- ./backend/topic_models.ipynb: For the same topic model code but in a jupyter notebook with some example outputs

### 6. Web Interface:

### Frontend:
- we built in react.js which contains the following components:
  - Header
  - Selection
  - Canvas
  - Navigation

### backend(APIS)
main.py: handles all the APIs and communicate the data with frontend. The code is in```./backend/main.py```


### Data:
- Spike Dectection data:
  - for each year and all years' hashtags, unigrams, word pairs are inside
    ```./backend/files```
    - For example: For 2016's hashtags:
      ```./backend/files/2016/hashtags_totalcounts_2016.csv```
- Event Dectection data:
  ```./backend/bucketsperdate.csv```

### 6. Team Member Contribution
- Mark Craft -  Topic Modeling,  Backend APIs, Frontend  
- Qinglin Chen -  Data cleaning, Vectorization, Backend APIs, Frontend  
- Lavanya Piramanayagam - Backend modules and feature implementation, Spike detection  
- Kavjit Durairaj - Data Prepration, Event detection, Spike detection  
