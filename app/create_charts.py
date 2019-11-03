import plotly.graph_objects as plotly
import base64
def makePie(percents):
    keys = []
    props = []
    for key in percents:
        keys.append(key)
        props.append(percents[key])
    
    data = plotly.Figure(data=[plotly.Pie(labels=keys, values=props)])
    chart = base64.b64encode(data.to_image(format="png"))
    return chart

percents = {}
percents["White"] = .25
percents["Black"] = .25
percents["Yellow"] = .25
percents["Brown"] = .25
chart = makePie(percents)
print(chart)