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
Our dataset in general poses two main challenges that make it difficult to detect spikes in the data. A global average would have a lot of noise and peaks computed based on this average would spike at points with no significant meaning. To address this issue, a dynamic value must be computed to allow detection of spikes in real-time. The algorithm we use is built on the 'smoothed z-score algorithm'; it takes in 3 input values, the lag, threshold and the influence. It constructs a moving mean and verifies if a data point is a certain number of standard deviation points away from the moving mean, this number of standard deviation is determined by the threshold variable. If it's a certain number of standard deviations away, we consider the data-point to be a spike. To determine how many data-points compute the moving mean, we use the lag variable. The influence decides how much impact the previous spike signal has on the detection at the current data-point. This algorithm proves to be very robust for our use case, as it constructs moving means and standard deviations that is capable of detecting spike values in the time-series for noisy twitter data. 
This concept was extended to both unigrams and word-pairs. To improve our results and provide better insight to users about the events trending on a particular day, we take the count of spikes on a per-day basis and provide users with the ability to filter based on individual dates. 

The code is structured as follows: 
main.py: contains the backend code to render our algorithms on our dataset files     
    csv_reader: Outputs the top 50 trend based on the file fed as input 
    thresholding_algo: Computers the array for spikes, average running mean and the standard deviation 
    plotter: Generates graphs for all the data including spikes
    

