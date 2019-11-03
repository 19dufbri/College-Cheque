import csv
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/results')
def results():
    return render_template("results.html", numResults=5)

finalData = []

def initalize():
	with open('data.csv') as csvDataFile:
    	reader = csv.DictReader(csvfile)
    	for row in reader:
        	finalData.append(processRow(row))

def processRow(row):
	newRow = {}
	newRow.append("name", row["INSTNM"])
	newRow.append("state", row["STABBR"])
	races = {}
	races.append("white", row["UGDS_WHITE"] / row["UGDS"])
	races.append("black", row["UGDS_BLACK"] / row["UGDS"])
	races.append("hispanic", row["UGDS_HISP"] / row["UGDS"])
	races.append("asian", row["UGDS_ASIAN"] / row["UGDS"])
	races.append("northnative", row["UGDS_AIAN"] / row["UGDS"])
	races.append("southnative", row["UGDS_NHPI"] / row["UGDS"])
	races.append("multi", row["UGDS_2MOR"] / row["UGDS"])
	races.append("nonresident", row["UGDS_NRA"] / row["UGDS"])
	races.append("unknown", row["UGDS_UNKN"] / row["UGDS"])
	newRow.append("racepercent", races)


if __name__ == '__main__':
    app.run(debug=False)
