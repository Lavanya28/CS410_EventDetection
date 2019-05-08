# CS410_EventDetection

Cleaner.py: 


## The first step of data preparation
### data_cleaning.py: 
####> remove urls, hashtags, stopwords, punctuation. 
####> lemmetize and stem each word
### 



Backend:
Topic Modeling: 

Spike Detection:
Our dataset in general has two main features that make it difficult to detect spikes in the data. The global average would have a lot of noise and peaks computed based on this average would spike at points with no significant meaning. To address this issue, a dynamic value must be computed to allow detection of spikes in real-time. The algorithm we use is built on the 'smoothed z-score algo', it takes in 3 input values lag, threshold and the influence. It constructs a moving mean and verifies if a data point is a certain number of standard deviation points away from the moving mean, this number of standard deviation is determined by the threshold variable. To determine how many datapoints compute the moving mean, we use the lag variable. The influence decides how much impact the previous signal has on the detection at the current datapoint. This algorithm proves to be very robust for our use case, as it constructs a moving mean and standard deviations,  

main.py:    
    csv_reader:
    thresholding_algo:
    plotter:
    

