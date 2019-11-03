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
    college["picture"] = makePie(college["racepercent"]).decode('utf-8')
    
    if json["degree"] == 1 or json["degree"] == 2:
        college["comp"] = college['C150_L4']
        college["reten"] = college['RET_FTL4']
    else:
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

    sumelems = 0
    numelems = 0
    if json["income"] == 1:
        numelems += 1
        sumelems += float(college["LO_INC_DEBT_MDN"])
    elif json["income"] == 2 or json["income"] == 3:
        numelems += 1
        sumelems += float(college["MD_INC_DEBT_MDN"])
    elif json["income"] == 4 or json["income"] == 5:
        numelems += 1
        sumelems += float(college["HI_INC_DEBT_MDN"])
    if json["dependent"] == "yes":
        numelems += 1
        sumelems += float(college["DEP_DEBT_MDN"])
    elif json["dependent"] == "no":
        numelems += 1
        sumelems += float(college["IND_DEBT_MDN"])
    if json["pell"] == "yes":
        numelems += 1
        sumelems += float(college["PELL_DEBT_MDN"])
    elif json["pell"] == "no":
        numelems += 1
        sumelems += float(college["NOPELL_DEBT_MDN"])
    if json["sex"] == "male":
        numelems += 1
        sumelems += float(college["MALE_DEBT_MDN"])
    elif json["sex"] == "female":
        numelems += 1
        sumelems += float(college["FEMALE_DEBT_MDN"])
    if json["firstGen"] == "yes":
        numelems += 1
        sumelems += float(college["FIRSTGEN_DEBT_MDN"])
    elif json["firstGen"] == "no":
        numelems += 1
        sumelems += float(college["NOFIRSTGEN_DEBT_MDN"])
    if numelems == 0:
        numelems = 1
        sumelems = float(college["GRAD_DEBT_MDN"])
    college["debt"] = sumelems / numelems
    
    sumelems = 0
    numelems = 0
    if json["income"] == 1:
        numelems += 1
        sumelems += float(college["LO_INC_RPY_1YR_RT"])
    elif json["income"] == 2 or json["income"] == 3:
        numelems += 1
        sumelems += float(college["MD_INC_RPY_1YR_RT"])
    elif json["income"] == 4 or json["income"] == 5:
        numelems += 1
        sumelems += float(college["HI_INC_RPY_1YR_RT"])
    if json["dependent"] == "yes":
        numelems += 1
        sumelems += float(college["DEP_RPY_1YR_RT"])
    elif json["dependent"] == "no":
        numelems += 1
        sumelems += float(college["IND_RPY_1YR_RT"])
    if json["pell"] == "yes":
        numelems += 1
        sumelems += float(college["PELL_RPY_1YR_RT"])
    elif json["pell"] == "no":
        numelems += 1
        sumelems += float(college["NOPELL_RPY_1YR_RT"])
    if json["sex"] == "male":
        numelems += 1
        sumelems += float(college["MALE_RPY_1YR_RT"])
    elif json["sex"] == "female":
        numelems += 1
        sumelems += float(college["FEMALE_RPY_1YR_RT"])
    if json["firstGen"] == "yes":
        numelems += 1
        sumelems += float(college["FIRSTGEN_RPY_1YR_RT"])
    elif json["firstGen"] == "no":
        numelems += 1
        sumelems += float(college["NOFIRSTGEN_RPY_1YR_RT"])
    if numelems == 0:
        numelems = 1
        sumelems = float(college["COMPL_RPY_1YR_RT"])
    college["one"] = sumelems / numelems

    sumelems = 0
    numelems = 0
    if json["income"] == 1:
        numelems += 1
        sumelems += float(college["LO_INC_RPY_3YR_RT"])
    elif json["income"] == 2 or json["income"] == 3:
        numelems += 1
        sumelems += float(college["MD_INC_RPY_3YR_RT"])
    elif json["income"] == 4 or json["income"] == 5:
        numelems += 1
        sumelems += float(college["HI_INC_RPY_3YR_RT"])
    if json["dependent"] == "yes":
        numelems += 1
        sumelems += float(college["DEP_RPY_3YR_RT"])
    elif json["dependent"] == "no":
        numelems += 1
        sumelems += float(college["IND_RPY_3YR_RT"])
    if json["pell"] == "yes":
        numelems += 1
        sumelems += float(college["PELL_RPY_3YR_RT"])
    elif json["pell"] == "no":
        numelems += 1
        sumelems += float(college["NOPELL_RPY_3YR_RT"])
    if json["sex"] == "male":
        numelems += 1
        sumelems += float(college["MALE_RPY_3YR_RT"])
    elif json["sex"] == "female":
        numelems += 1
        sumelems += float(college["FEMALE_RPY_3YR_RT"])
    if json["firstGen"] == "yes":
        numelems += 1
        sumelems += float(college["FIRSTGEN_RPY_3YR_RT"])
    elif json["firstGen"] == "no":
        numelems += 1
        sumelems += float(college["NOFIRSTGEN_RPY_3YR_RT"])
    if numelems == 0:
        numelems = 1
        sumelems = float(college["GRAD_RPY_3YR_RT"])
    college["three"] = sumelems / numelems

    sumelems = 0
    numelems = 0
    if json["income"] == 1:
        numelems += 1
        sumelems += float(college["LO_INC_RPY_5YR_RT"])
    elif json["income"] == 2 or json["income"] == 3:
        numelems += 1
        sumelems += float(college["MD_INC_RPY_5YR_RT"])
    elif json["income"] == 4 or json["income"] == 5:
        numelems += 1
        sumelems += float(college["HI_INC_RPY_5YR_RT"])
    if json["dependent"] == "yes":
        numelems += 1
        sumelems += float(college["DEP_RPY_5YR_RT"])
    elif json["dependent"] == "no":
        numelems += 1
        sumelems += float(college["IND_RPY_5YR_RT"])
    if json["pell"] == "yes":
        numelems += 1
        sumelems += float(college["PELL_RPY_5YR_RT"])
    elif json["pell"] == "no":
        numelems += 1
        sumelems += float(college["NOPELL_RPY_5YR_RT"])
    if json["sex"] == "male":
        numelems += 1
        sumelems += float(college["MALE_RPY_5YR_RT"])
    elif json["sex"] == "female":
        numelems += 1
        sumelems += float(college["FEMALE_RPY_5YR_RT"])
    if json["firstGen"] == "yes":
        numelems += 1
        sumelems += float(college["FIRSTGEN_RPY_5YR_RT"])
    elif json["firstGen"] == "no":
        numelems += 1
        sumelems += float(college["NOFIRSTGEN_RPY_5YR_RT"])
    if numelems == 0:
        numelems = 1
        sumelems = float(college["COMPL_RPY_5YR_RT"])
    college["five"] = sumelems / numelems

    sumelems = 0
    numelems = 0
    if json["income"] == 1:
        numelems += 1
        sumelems += float(college["LO_INC_RPY_7YR_RT"])
    elif json["income"] == 2 or json["income"] == 3:
        numelems += 1
        sumelems += float(college["MD_INC_RPY_7YR_RT"])
    elif json["income"] == 4 or json["income"] == 5:
        numelems += 1
        sumelems += float(college["HI_INC_RPY_7YR_RT"])
    if json["dependent"] == "yes":
        numelems += 1
        sumelems += float(college["DEP_RPY_7YR_RT"])
    elif json["dependent"] == "no":
        numelems += 1
        sumelems += float(college["IND_RPY_7YR_RT"])
    if json["pell"] == "yes":
        numelems += 1
        sumelems += float(college["PELL_RPY_7YR_RT"])
    elif json["pell"] == "no":
        numelems += 1
        sumelems += float(college["NOPELL_RPY_7YR_RT"])
    if json["sex"] == "male":
        numelems += 1
        sumelems += float(college["MALE_RPY_7YR_RT"])
    elif json["sex"] == "female":
        numelems += 1
        sumelems += float(college["FEMALE_RPY_7YR_RT"])
    if json["firstGen"] == "yes":
        numelems += 1
        sumelems += float(college["FIRSTGEN_RPY_7YR_RT"])
    elif json["firstGen"] == "no":
        numelems += 1
        sumelems += float(college["NOFIRSTGEN_RPY_7YR_RT"])
    if numelems == 0:
        numelems = 1
        sumelems = float(college["COMPL_RPY_7YR_RT"])
    college["seven"] = sumelems / numelems

    if json["degree"] == 1 or json["degree"] == 2:
        if json["race"] == "white":
            college["estim"] = college["C150_L4_WHITE"]
        elif json["race"] == "black":
            college["estim"] = college["C150_L4_BLACK"]
        elif json["race"] == "hispanic":
            college["estim"] = college["C150_L4_HISP"]
        elif json["race"] == "asian":
            college["estim"] = college["C150_L4_ASIAN"]
        elif json["race"] == "northNative":
            college["estim"] = college["C150_L4_AIAN"]
        elif json["race"] == "southNative":
            college["estim"] = college["C150_L4_NHPI"]
        elif jsom["race"] == "twoOrMore":
            college["estim"] = college["C150_L4_2MOR"]
        elif json["race"] == "nonResAlien":
            college["estim"] = college["C150_L4_NRA"]
        elif json["race"] == "unknown":
            college["estim"] = college["C150_L4_UNKN"]
        else:
            college["estim"] = college["C150_L4"]
    else:
        if json["race"] == "white":
            college["estim"] = college["C150_4_WHITE"]
        elif json["race"] == "black":
            college["estim"] = college["C150_4_BLACK"]
        elif json["race"] == "hispanic":
            college["estim"] = college["C150_4_HISP"]
        elif json["race"] == "asian":
            college["estim"] = college["C150_4_ASIAN"]
        elif json["race"] == "northNative":
            college["estim"] = college["C150_4_AIAN"]
        elif json["race"] == "southNative":
            college["estim"] = college["C150_4_NHPI"]
        elif jsom["race"] == "twoOrMore":
            college["estim"] = college["C150_4_2MOR"]
        elif json["race"] == "nonResAlien":
            college["estim"] = college["C150_4_NRA"]
        elif json["race"] == "unknown":
            college["estim"] = college["C150_4_UNKN"]
        else:
            college["estim"] = college["C150_4"]
    
    sumelems = 0
    numelems = 0
    if json["dependent"] == "yes":
        numelems += 1
        sumelems += float(college["MN_EARN_WNE_INDEP0_P10"])
    elif json["dependent"] == "no":
        numelems += 1
        sumelems += float(college["MN_EARN_WNE_INDEP1_P10"])
    if json["sex"] == "male":
        numelems += 1
        sumelems += float(college["MN_EARN_WNE_MALE1_P10"])
    elif json["sex"] == "female":
        numelems += 1
        sumelems += float(college["MN_EARN_WNE_MALE0_P10"])
    if numelems == 0:
        numelems = 1
        sumelems = float(college["MN_EARN_WNE_P10"])
    college["ten"] = sumelems / numelems;


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
