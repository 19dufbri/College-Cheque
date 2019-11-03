import matplotlib.pyplot as plt
import base64
from io import StringIO

def makePie(dict):
    labels = []
    percents = []
    colors = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9"]
    for k, v in dict.items():
        labels.append(k)
        percents.append(v)

    plt.pie(percents, labels=labels, colors=colors, startangle=90,frame=True)


    buffer = StringIO.StringIO();
    plt.savefig(buffer, format="jpg")
    buffer.seek(0)
    return base64.b64encode(buffer.read())
