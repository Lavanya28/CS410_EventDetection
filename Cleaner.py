import os
import pandas 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import re


files = os.listdir("1000/")
stop_words = set(stopwords.words('english')) 

for file in files:
	data = pandas.read_csv('1000/'+file)
	everyfile = (list(data['text']))
	text_file = open("text/"+file.replace('.csv','') +".txt", 'a')
	for line in everyfile:
		
		line = re.sub(r"\S*http\S*", "", line)
		line = re.sub(r"#\S+", "", line)
		word_list = line.split(" ")
		
		
		new_line=""

		for word in word_list:
			word = word.lower()
			if word  not in stop_words:
				new_line = new_line+word+ " "

		
		text_file.write(new_line + "\n")

		
		
	
		
		
	

	




