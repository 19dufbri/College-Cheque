import plotly.graph_objects as plotly
import base64
import csv
from flask import Flask, render_template, url_for, request, jsonify
app = Flask(__name__)

finalData = []
names = []

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/results')
def results():
    name = ""
    results = []
    json = json.loads(request.cookies.get("college-input-data", "{}"))
    for college in finalData:
        if college["name"] == name:
            results.append(getPersonalData(college))
    return render_template("results.html", results=results)

def getPersonalData(json, college):
    college["picture"] = makePie(college["racepercent"])
    
    if json["degree"] == 1:
        college["comp"] = college['C150_L4']
        college["reten"] = college['RET_FTL4']
    elif json["degree"] == 2:
        college["comp"] = college['C150_L4']
        college["reten"] = college['RET_FTL4']
    else
        college["comp"] = college['C150_4']
        college["reten"] = college['RET_FT4']

    college["net"] = college["tuition"][json["income"]]

    if college["TUITIONFEE_PROG"] == "NULL":
        if college["STABBR"] == json["state"]:
            college["tuition"] = college["TUITIONFEE_IN"]
        else:
            college["tuition"] = college["TUITIONFEE_OUT"]
    else:
        college["tuition"] = college["TUITIONFEE_PROG"];

    college["pell"]

    return college


def initalize():
    with open('data.csv') as csvDataFile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            finalData.append(processRow(row))
            names.append(row["INSTNM"])

def processRow(row):
    races = {}
    races["White"] = row["UGDS_WHITE"]
    races["Black"] = row["UGDS_BLACK"]
    races["Hispanic"] = row["UGDS_HISP"]
    races["Asian"] = row["UGDS_ASIAN"]
    races["Am. Indian"] = row["UGDS_AIAN"]
    races["Hawiian/PI"] = row["UGDS_NHPI"]
    races["Two or more"] = row["UGDS_2MOR"]
    races["Non-resident"] = row["UGDS_NRA"] 
    races["Unknown"] = row["UGDS_UNKN"]
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
    
    data = plotly.Figure(data = [plotly.Pie(labels = keys, values = props, hole = .375, sort = False)])
    colors = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9"]
    data.update_traces(direction = "clockwise", textinfo = "percent", textfont_size = 20, marker = dict(colors = colors))
    data.update_layout(autosize = False, width = 650, height = 650, legend = dict(y = .5, font = dict(size = 20)))
    data.update_layout(margin = plotly.layout.Margin(l = 0, r = 0, t = 0, b = 0), paper_bgcolor = "#fbfaf6")
    chart = base64.b64encode(data.to_image(format = "png"))
    return chart

if __name__ == '__main__':
    app.run(debug=False)
