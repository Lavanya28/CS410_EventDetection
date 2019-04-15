import os
import pandas 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import re
import string 


files = os.listdir("sorted_26/")
stop_words = set(stopwords.words('english')) 
print (files)
for file in files:
	
	data = pandas.read_csv('sorted_26/'+file)
	print('sorted_26/'+file) 
	try:
		everyfile = (list(data['text']))
	except: 
		continue 
	
	text_file = open("text/"+file.replace('.csv','') +".txt", 'a')
	for line in everyfile:
		
		line = re.sub(r"\S*http\S*", "", line)
		line = re.sub(r"#\S+", "", line)
		remove = dict.fromkeys(map(ord, string.punctuation))
		line = line.translate(remove)
		word_list = line.split(" ")
		
		
		new_line=""

		for word in word_list:
			word = word.lower()
			if word  not in stop_words:
				new_line = new_line+word+ " "

		
		text_file.write(new_line + "\n\n")

		
		
	
		
		
	

	




