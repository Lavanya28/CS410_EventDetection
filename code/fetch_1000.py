import os
idlist = [] 
with open('tweets_3200/top1000.txt') as f:
		content = f.readlines()


for i in content: 
	val = i.split("\t")
	val = val[1]
	idlist.append(val)

#print(idlist)
count = 0
for ids in idlist:
	string = "tweets_3200/" + ids + ".csv"
	print (string)
	if (os.path.isfile(string)):
		
		os.rename(string, "1000"+ids+".csv")
		
