import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt

excel_conf = {
    "Ball": {
        "TP": 3,
        "FP": 1,
        "FN": 14,
        "o": []
    },
    "Vase": {
        "TP": 19,
        "FP": 2,
        "FN": 1,
        "o": []
    },
    "Corona": {
        "TP": 5,
        "FP": 1,
        "FN": 2,
        "o": []
    },
    "Red": {
        "TP": 10,
        "FP": 2,
        "FN": 7,
        "o": []
    },
    "Crown": {
        "TP": 6,
        "FP": 0,
        "FN": 1,
        "o": []
    },
    "Grey_white": {
        "TP": 1,
        "FP": 0,
        "FN": 5,
        "o": []
    }
}

excel_conf = {
    "A": {
        "TP": 15,
        "FP": 2,
        "FN": 3,
        "o": []
    },
    "B": {
        "TP": 8,
        "FP": 0,
        "FN": 1,
        "o": []
    },
    "C": {
        "TP": 5,
        "FP": 1,
        "FN": 0,
        "o": ["A"]
    },
    "D": {
        "TP": 8,
        "FP": 0,
        "FN": 0,
        "o": []
    }
}

data = {
    "y_actual": [],
    "y_predicted": []
}

for k,v in excel_conf.items():
    tp = [k]*v["TP"]
    data["y_actual"] += tp
    data["y_predicted"] += tp

    fp_a = ["background FP"]*v["FP"]
    fp_p = [k]*v["FP"]
    data["y_actual"] += fp_a
    data["y_predicted"] += fp_p

    fn_a = [k]*v["FN"]
    fn_p = ["background FN"]*v["FN"]
    data["y_actual"] += fn_a
    data["y_predicted"] += fn_p

    if len(v["o"]) > 0:
        o_a = [k]*len(v["o"])
        o_p = v["o"]
        data["y_actual"] += o_a
        data["y_predicted"] += o_p

df = pd.DataFrame(data, columns=['y_actual','y_predicted'])
confusion_matrix = pd.crosstab(df['y_actual'], df['y_predicted'], rownames=['Actual'], colnames=['Predicted'], margins=False, normalize="index")

index_order = ["Ball", "Vase", "Corona", "Red", "Crown", "Grey_white", "background FP"]
columns_order = ["Ball", "Vase", "Corona", "Red", "Crown", "Grey_white", "background FN"]

index_order = ["A", "B", "C", "D", "background FP"]
columns_order = ["A", "B", "C", "D", "background FN"]

confusion_matrix = confusion_matrix.reindex(index_order, columns=columns_order)
#confusion_matrix_norm = confusion_matrix / confusion_matrix.sum(axis=1)

plt.figure(figsize=(8.21, 7.03), dpi=120)
ax = sn.heatmap(confusion_matrix, annot=True, cmap='viridis', vmin=0, vmax=1)
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')

plt.xlabel("Prédiction", fontsize=16, labelpad=-10)
plt.ylabel("Réalité", fontsize=16)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(rotation=45, fontsize=12)


plt.tight_layout()
plt.savefig("fig1.png", dpi=120)

plt.show()