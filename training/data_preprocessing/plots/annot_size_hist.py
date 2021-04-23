import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

sizes_w = []
sizes_h = []

with open("../annotations/Ifremer_v4.csv", encoding="utf-8") as f:
    lines = [l.rstrip("\n") for l in f.readlines()]

for i, l in enumerate(lines) :
    if i == 0:
        continue

    s = l.split(";")
    points = json.loads(s[13])
    attr = s[14].replace("\"\"", "\"")[1:-1]
    attr = json.loads(attr)

    d = points[2]
    relative_dw = d/attr["width"]
    relative_dh = d/attr["height"]

    sizes_w.append(relative_dw)
    sizes_h.append(relative_dh)


df = pd.Series(sizes_w)
print(len(sizes_w))
hist = df.hist(bins=18, color="#3C8FBC", edgecolor="#0F355B", linewidth=1.1)
hist.grid(False)

plt.axvline(df.mean(), color='k', linestyle='dashed', linewidth=1)
min_ylim, max_ylim = plt.ylim()
plt.text(df.mean()*1.1, max_ylim*0.9, 'Moyenne : {:.3f}'.format(df.mean()))

plt.xlabel("Diamètre relatif de l'annotation par rapport à la largeur de l'image", fontsize=16)
plt.ylabel("Nombre d'annotations", fontsize=16)
plt.xticks(fontsize=12)  
plt.yticks(fontsize=12)  

plt.show()