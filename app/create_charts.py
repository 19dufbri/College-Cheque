import plotly.graph_objects as plotly
import base64
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

percents = {}
percents["White"] = 124
percents["Black"] = 395
percents["Hispanic"] = 239
percents["Asian"] = 673
percents["Am. Indian"] = 129
percents["Hawaiian/PI"] = 548
percents["Two or more"] = 379
percents["Non-resident"] = 495
percents["Unknown"] = 216
chart = makePie(percents)
print(chart)