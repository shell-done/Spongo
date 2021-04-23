import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

classes = {
    "Vase": {
        "nb": 0,
        "color": "#A249A5"
    },
    "Ball": {
        "nb": 0,
        "color": "#99CA53"
    },
    "Corona": {
        "nb": 0,
        "color": "#F6A625"
    },
    "Red": {
        "nb": 0,
        "color": "#BC3F38"
    },
    "Crown": {
        "nb": 0,
        "color": "#117FB2"
    },
    "Grey_white": {
        "nb": 0,
        "color": "#000062"
    }
}

with open("../annotations/Ifremer_v4.csv", encoding="utf-8") as f:
    lines = [l.rstrip("\n") for l in f.readlines()]

for i, l in enumerate(lines) :
    if i == 0:
        continue
    
    s = l.split(";")
    c = s[2]

    classes[c]["nb"] += 1

labels = list(classes.keys())
val = [c["nb"] for c in classes.values()]
col = [c["color"] for c in classes.values()]

bar = plt.barh(labels, val, color=col)
plt.xlabel("Nombre d'annotations", fontsize=16)
plt.ylabel("Morphotypes", fontsize=16)
plt.xticks(fontsize=12)  
plt.yticks(fontsize=12)  

plt.show()