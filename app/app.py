import base64
import csv
import json
from flask import Flask, render_template, url_for, request, jsonify, redirect
import matplotlib.pyplot as plt
from io import BytesIO
from flask import jsonify
import numpy as np

app = Flask(__name__)

finalData = []
names = []

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/results')
def results():
    results = []
    if (request.cookies.get("college-input-data") is None):
        return redirect("/", code=302)
    jsondata = json.loads(request.cookies.get("college-input-data"))
    for college in finalData:
        if college["INSTNM"] in jsondata["collegeNames"]:
            results.append(getPersonalData(jsondata, college))
    return render_template("results.html", numres=len(results), results=results)

@app.route('/autocomplete',methods=['GET'])
def autocomplete():
    search = request.args.get('term')
    app.logger.debug(search)
    return jsonify(json_list=names)


def getPersonalData(json, college):
    college["picture"] = makePie(college["racepercent"])

    if json["degree"] == "1" or json["degree"] == "2":
        college["comp"] = int(100 * getFloat(college, "C150_L4"))
        college["reten"] = int(100 * getFloat(college, "RET_FTL4"))
    else:
        college["comp"] = int(100 * getFloat(college, "C150_4"))
        college["reten"] = int(100 * getFloat(college, "RET_FT4"))

    incomeNum = json["income"]
    tuition = college["price"]
    college["net"] = tuition[incomeNum]

    college["pell"] = int(100 * getFloat(college, "PCTPELL"))
    college["loan"] = int(100 * getFloat(college, "PCTFLOAN"))

    if college["TUITIONFEE_PROG"] == "NULL":
        if college["STABBR"] == json["state"]:
            college["tuition"] = getString(college, "TUITIONFEE_IN")
        else:
            college["tuition"] = getString(college, "TUITIONFEE_OUT")
    else:
        college["tuition"] = getString(college, "TUITIONFEE_PROG")

    sumelems = 0
    numelems = 0
    if json["income"] == 1:
        numelems += 1
        sumelems += getFloat(college, "LO_INC_DEBT_MDN")
    elif json["income"] == 2 or json["income"] == 3:
        numelems += 1
        sumelems += getFloat(college, "MD_INC_DEBT_MDN")
    elif json["income"] == 4 or json["income"] == 5:
        numelems += 1
        sumelems += getFloat(college, "HI_INC_DEBT_MDN")
    if json["dependent"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "DEP_DEBT_MDN")
    elif json["dependent"] == "no":
        numelems += 1
        sumelems += getFloat(college, "IND_DEBT_MDN")
    if json["pell"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "PELL_DEBT_MDN")
    elif json["pell"] == "no":
        numelems += 1
        sumelems += getFloat(college, "NOPELL_DEBT_MDN")
    if json["sex"] == "male":
        numelems += 1
        sumelems += getFloat(college, "MALE_DEBT_MDN")
    elif json["sex"] == "female":
        numelems += 1
        sumelems += getFloat(college, "FEMALE_DEBT_MDN")
    if json["firstGen"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "FIRSTGEN_DEBT_MDN")
    elif json["firstGen"] == "no":
        numelems += 1
        sumelems += getFloat(college, "NOTFIRSTGEN_DEBT_MDN")
    if numelems == 0:
        numelems = 1
        sumelems = getFloat(college, "GRAD_DEBT_MDN")
    college["debt"] = int(sumelems / numelems)
    
    sumelems = 0
    numelems = 0
    if json["income"] == 1:
        numelems += 1
        sumelems += getFloat(college, "LO_INC_RPY_1YR_RT")
    elif json["income"] == 2 or json["income"] == 3:
        numelems += 1
        sumelems += getFloat(college, "MD_INC_RPY_1YR_RT")
    elif json["income"] == 4 or json["income"] == 5:
        numelems += 1
        sumelems += getFloat(college, "HI_INC_RPY_1YR_RT")
    if json["dependent"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "DEP_RPY_1YR_RT")
    elif json["dependent"] == "no":
        numelems += 1
        sumelems += getFloat(college, "IND_RPY_1YR_RT")
    if json["pell"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "PELL_RPY_1YR_RT")
    elif json["pell"] == "no":
        numelems += 1
        sumelems += getFloat(college, "NOPELL_RPY_1YR_RT")
    if json["sex"] == "male":
        numelems += 1
        sumelems += getFloat(college, "MALE_RPY_1YR_RT")
    elif json["sex"] == "female":
        numelems += 1
        sumelems += getFloat(college, "FEMALE_RPY_1YR_RT")
    if json["firstGen"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "FIRSTGEN_RPY_1YR_RT")
    elif json["firstGen"] == "no":
        numelems += 1
        sumelems += getFloat(college, "NOTFIRSTGEN_RPY_1YR_RT")
    if numelems == 0:
        numelems = 1
        sumelems = getFloat(college, "COMPL_RPY_1YR_RT")
    college["one"] = int(100 * sumelems / numelems)

    sumelems = 0
    numelems = 0
    if json["income"] == 1:
        numelems += 1
        sumelems += getFloat(college, "LO_INC_RPY_3YR_RT")
    elif json["income"] == 2 or json["income"] == 3:
        numelems += 1
        sumelems += getFloat(college, "MD_INC_RPY_3YR_RT")
    elif json["income"] == 4 or json["income"] == 5:
        numelems += 1
        sumelems += getFloat(college, "HI_INC_RPY_3YR_RT")
    if json["dependent"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "DEP_RPY_3YR_RT")
    elif json["dependent"] == "no":
        numelems += 1
        sumelems += getFloat(college, "IND_RPY_3YR_RT")
    if json["pell"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "PELL_RPY_3YR_RT")
    elif json["pell"] == "no":
        numelems += 1
        sumelems += getFloat(college, "NOPELL_RPY_3YR_RT")
    if json["sex"] == "male":
        numelems += 1
        sumelems += getFloat(college, "MALE_RPY_3YR_RT")
    elif json["sex"] == "female":
        numelems += 1
        sumelems += getFloat(college, "FEMALE_RPY_3YR_RT")
    if json["firstGen"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "FIRSTGEN_RPY_3YR_RT")
    elif json["firstGen"] == "no":
        numelems += 1
        sumelems += getFloat(college, "NOTFIRSTGEN_RPY_3YR_RT")
    if numelems == 0:
        numelems = 1
        sumelems = getFloat(college, "GRAD_RPY_3YR_RT")
    college["three"] = int(100 * sumelems / numelems)

    sumelems = 0
    numelems = 0
    if json["income"] == 1:
        numelems += 1
        sumelems += getFloat(college, "LO_INC_RPY_5YR_RT")
    elif json["income"] == 2 or json["income"] == 3:
        numelems += 1
        sumelems += getFloat(college, "MD_INC_RPY_5YR_RT")
    elif json["income"] == 4 or json["income"] == 5:
        numelems += 1
        sumelems += getFloat(college, "HI_INC_RPY_5YR_RT")
    if json["dependent"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "DEP_RPY_5YR_RT")
    elif json["dependent"] == "no":
        numelems += 1
        sumelems += getFloat(college, "IND_RPY_5YR_RT")
    if json["pell"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "PELL_RPY_5YR_RT")
    elif json["pell"] == "no":
        numelems += 1
        sumelems += getFloat(college, "NOPELL_RPY_5YR_RT")
    if json["sex"] == "male":
        numelems += 1
        sumelems += getFloat(college, "MALE_RPY_5YR_RT")
    elif json["sex"] == "female":
        numelems += 1
        sumelems += getFloat(college, "FEMALE_RPY_5YR_RT")
    if json["firstGen"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "FIRSTGEN_RPY_5YR_RT")
    elif json["firstGen"] == "no":
        numelems += 1
        sumelems += getFloat(college, "NOTFIRSTGEN_RPY_5YR_RT")
    if numelems == 0:
        numelems = 1
        sumelems = getFloat(college, "COMPL_RPY_5YR_RT")
    college["five"] = int(100 * sumelems / numelems)

    sumelems = 0
    numelems = 0
    if json["income"] == 1:
        numelems += 1
        sumelems += getFloat(college, "LO_INC_RPY_7YR_RT")
    elif json["income"] == 2 or json["income"] == 3:
        numelems += 1
        sumelems += getFloat(college, "MD_INC_RPY_7YR_RT")
    elif json["income"] == 4 or json["income"] == 5:
        numelems += 1
        sumelems += getFloat(college, "HI_INC_RPY_7YR_RT")
    if json["dependent"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "DEP_RPY_7YR_RT")
    elif json["dependent"] == "no":
        numelems += 1
        sumelems += getFloat(college, "IND_RPY_7YR_RT")
    if json["pell"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "PELL_RPY_7YR_RT")
    elif json["pell"] == "no":
        numelems += 1
        sumelems += getFloat(college, "NOPELL_RPY_7YR_RT")
    if json["sex"] == "male":
        numelems += 1
        sumelems += getFloat(college, "MALE_RPY_7YR_RT")
    elif json["sex"] == "female":
        numelems += 1
        sumelems += getFloat(college, "FEMALE_RPY_7YR_RT")
    if json["firstGen"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "FIRSTGEN_RPY_7YR_RT")
    elif json["firstGen"] == "no":
        numelems += 1
        sumelems += getFloat(college, "NOTFIRSTGEN_RPY_7YR_RT")
    if numelems == 0:
        numelems = 1
        sumelems = getFloat(college, "COMPL_RPY_7YR_RT")
    college["seven"] = int(100 * sumelems / numelems)

    if json["degree"] == 1 or json["degree"] == 2:
        if json["race"] == "white":
            college["estim"] = getFloat(college, "C150_L4_WHITE")
        elif json["race"] == "black":
            college["estim"] = getFloat(college, "C150_L4_BLACK")
        elif json["race"] == "hispanic":
            college["estim"] = getFloat(college, "C150_L4_HISP")
        elif json["race"] == "asian":
            college["estim"] = getFloat(college, "C150_L4_ASIAN")
        elif json["race"] == "northNative":
            college["estim"] = getFloat(college, "C150_L4_AIAN")
        elif json["race"] == "southNative":
            college["estim"] = getFloat(college, "C150_L4_NHPI")
        elif json["race"] == "twoOrMore":
            college["estim"] = getFloat(college, "C150_L4_2MOR")
        elif json["race"] == "nonResAlien":
            college["estim"] = getFloat(college, "C150_L4_NRA")
        elif json["race"] == "unknown":
            college["estim"] = getFloat(college, "C150_L4_UNKN")
        else:
            college["estim"] = getFloat(college, "C150_L4")
    else:
        if json["race"] == "white":
            college["estim"] = getFloat(college, "C150_4_WHITE")
        elif json["race"] == "black":
            college["estim"] = getFloat(college, "C150_4_BLACK")
        elif json["race"] == "hispanic":
            college["estim"] = getFloat(college, "C150_4_HISP")
        elif json["race"] == "asian":
            college["estim"] = getFloat(college, "C150_4_ASIAN")
        elif json["race"] == "northNative":
            college["estim"] = getFloat(college, "C150_4_AIAN")
        elif json["race"] == "southNative":
            college["estim"] = getFloat(college, "C150_4_NHPI")
        elif json["race"] == "twoOrMore":
            college["estim"] = getFloat(college, "C150_4_2MOR")
        elif json["race"] == "nonResAlien":
            college["estim"] = getFloat(college, "C150_4_NRA")
        elif json["race"] == "unknown":
            college["estim"] = getFloat(college, "C150_4_UNKN")
        else:
            college["estim"] = getFloat(college, "C150_4")
    college["estim"] = int(college["estim"] * 100)
    
    sumelems = 0
    numelems = 0
    if json["dependent"] == "yes":
        numelems += 1
        sumelems += getFloat(college, "MN_EARN_WNE_INDEP0_P10")
    elif json["dependent"] == "no":
        numelems += 1
        sumelems += getFloat(college, "MN_EARN_WNE_INDEP1_P10")
    if json["sex"] == "male":
        numelems += 1
        sumelems += getFloat(college, "MN_EARN_WNE_MALE1_P10")
    elif json["sex"] == "female":
        numelems += 1
        sumelems += getFloat(college, "MN_EARN_WNE_MALE0_P10")
    if numelems == 0:
        numelems = 1
        sumelems = getFloat(college, "MN_EARN_WNE_P10")
    college["ten"] = int(sumelems / numelems);

    return college


def initalize():
    with open('app/data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            finalData.append(processRow(row))
            names.append(row["INSTNM"])

def processRow(row):
    races = {}
    races["White"] = getFloat(row, "UGDS_WHITE")
    races["Black"] = getFloat(row, "UGDS_BLACK")
    races["Hispanic"] = getFloat(row, "UGDS_HISP")
    races["Asian"] = getFloat(row, "UGDS_ASIAN")
    races["Am. Indian"] = getFloat(row, "UGDS_AIAN")
    races["Hawiian/PI"] = getFloat(row, "UGDS_NHPI")
    races["Two or more"] = getFloat(row, "UGDS_2MOR")
    races["Non-resident"] = getFloat(row, "UGDS_NRA") 
    races["Unknown"] = getFloat(row, "UGDS_UNKN")
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
    row["price"] = tuition
    return row

def makePie(dict):
    plt.figure()
    labels = []
    percents = []
    colors = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9"]
    for k, v in dict.items():
        labels.append(k)
        percents.append(v)

    patches, texts, misc = plt.pie(percents, colors=colors, autopct='%1.1f%%', startangle=90, pctdistance=1.1)
    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')
    plt.tight_layout()
    plt.legend(patches, labels, loc="best")
    buf = BytesIO();
    plt.savefig(buf)
    buf.seek(0)
    labels = []
    percents = []
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def getFloat(college, field):
    if college[field] == "NULL" or college[field] == "PrivacySuppressed":
        return 0.0
    return float(college[field])

def getString(college, field):
    if college[field] == "NULL" or college[field] == "PrivacySuppressed":
        return "N/A"
    return college[field]

def makeScatter(dict1, dict2):
    labels = []
    avgCost = []
    percents = []
    colors = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9"]
    for k, v in dict1.items():
        labels.append(k)
        percents.append(v)

    patches, texts = plt.pie(percents, colors=colors, startangle=90,frame=false)
    plt.legend(patches, labels, loc="best")
    buffer = BytesIO();
    plt.savefig(buffer, format="jpg")
    buffer.seek(0)
    return base64.b64encode(buffer.read())

initalize()

if __name__ == '__main__':
    app.run(debug=False)
else:
    application = app