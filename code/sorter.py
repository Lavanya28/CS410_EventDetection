import sys,csv, operator
data = csv.reader(open('out.csv'), delimiter=',')
sortedlist = sorted(data, key = operator.itemgetter(1))
with open("sorted.csv", "w") as f:
	fileWriter = csv.writer(f,delimiter=',')
	for row in sortedlist:
		fileWriter.writerow(row)



