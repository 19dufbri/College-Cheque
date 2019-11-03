import plotly.graph_objects as plotly
import base64
import csv
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/results')
def results():
    name = ""
    results = []
    for college in finalData:
        if college["name"] == name:
            college["picture"] = makePie(college["racepercent"])
            results.append(college)
    return render_template("results.html", results=results)

finalData = []

def initalize():
    with open('data.csv') as csvDataFile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            finalData.append(processRow(row))

def processRow(row):
    races = {}
    races["White"] = row["UGDS_WHITE"]
    races["Black"] = row["UGDS_BLACK"]
    races["Hispanic"] = row["UGDS_HISP"]
    races["Asian"] = row["UGDS_ASIAN"]
    races["American Indian and Alaskan Native"] = row["UGDS_AIAN"]
    races["Native Hawiian and Pacific Islander"] = row["UGDS_NHPI"]
    races["Two or More"] = row["UGDS_2MOR"]
    races["Nonresident Alien"] = row["UGDS_NRA"] 
    races["Unkown"] = row["UGDS_UNKN"]
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
    row["tuition"] = tuition
    return row

def makePie(percents):
    keys = []
    props = []
    for key in percents:
        keys.append(key)
        props.append(percents[key])
    data = plotly.Figure(data=[plotly.Pie(labels=keys, values=props)])
    chart = base64.b64encode(data.to_image(format="png"))
    return chart

if __name__ == '__main__':
    app.run(debug=False)
