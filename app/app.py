import csv
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/results')
def results():
    return render_template("results.html", numResults=5)

def initalize():
	with open('file.csv') as csvDataFile:
    	csvReader = csv.reader(csvDataFile)
    	for row in csvReader:
        	print(row)

if __name__ == '__main__':
    app.run(debug=False)
