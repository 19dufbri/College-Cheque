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
    races = {}
    races["white"] = row["UGDS_WHITE"]
    races["black"] = row["UGDS_BLACK"]
    races["hispanic"] = row["UGDS_HISP"]
    races["asian"] = row["UGDS_ASIAN"]
    races["northnative"] = row["UGDS_AIAN"]
    races["southnative"] = row["UGDS_NHPI"]
    races["multi"] = row["UGDS_2MOR"]
    races["nonresident"] = row["UGDS_NRA"] 
    races["unknown"] = row["UGDS_UNKN"]
    row["racepercent"] = races
    tuition = {}
    if row["NPT4_PUB"] != "NULL":
        tuition["0"] = row["NPT4_PUB"]
        tuition["1"] = row["NPT41_PUB"]
        tuition["2"] = row["NPT42_PUB"]
        tuition["3"] = row["NPT43_PUB"]
        tuition["4"] = row["NPT44_PUB"]
        tuition["5"] = row["NPT45_PUB"]
    else:
        tuition["0"] = row["NPT4_PRIV"]
        tuition["1"] = row["NPT41_PRIV"]
        tuition["2"] = row["NPT42_PRIV"]
        tuition["3"] = row["NPT43_PRIV"]
        tuition["4"] = row["NPT44_PRIV"]
        tuition["5"] = row["NPT45_PRIV"]
    row["racepercent"] = tuition


if __name__ == '__main__':
    app.run(debug=False)
