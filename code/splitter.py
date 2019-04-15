f = open("sorted.csv")

filename = 1
count = 1
fout = open(str(filename)+".csv", "a")

for line in f:
		if(count==145347):
			count = 1
			filename=filename+1
			fout = open(str(filename)+".csv", "a")
		
		fout.write(line)
		count +=1