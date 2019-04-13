# merge file name
import os
fout = open("merged.csv", "a")

# read all files in 1000

list_of_files = os.listdir("1000/")


print (list_of_files)

#print ((files))

#list_of_files=['10005380672.csv', '10007092102.csv' ]



for file in list_of_files:
	f = open("1000/"+ file)
	f.__next__()
	for line in f:
		fout.write(line)
	f.close()

fout.close()

