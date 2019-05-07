from flask import Flask, render_template, request
import csv
import operator

app = Flask(__name__)

def csv_reader(filename):
	reader = csv.reader(open(filename))  
	result = {}
	for row in reader:
		key = row[0]
		result[key] = int(row[1])
	sorted_result = sorted(result.items(), key=operator.itemgetter(1))
	sorted_result = sorted_result[::-1]

	return (sorted_result[0:50])



@app.route("/", methods = ['POST', 'GET'])
def home():
	if request.method == 'POST':
		if request.form['top'] == 'Top trending Hastags':
			result = csv_reader('hashtag_counts.csv')
			return render_template("home.html", result=result)
	            
		elif request.form['top'] == 'Top trending Words':

			return render_template("home.html")


		elif request.form['top'] == 'Top trending Word-pairs':

			return render_template("home.html")

		else:
			pass
            
	return render_template("home.html")




if __name__ == "__main__":
    app.run(debug=True)