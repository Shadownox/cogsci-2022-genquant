import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

from correct_conclusions import correct_conclusions as cc

# Load dataset
data_df = pd.read_csv("../data/Ragni2021.csv")

# Get valid syllogisms
valid_syls = []
for key in cc.keys():
    if cc[key] != ["NVC"]:
        valid_syls.append(key)

# Define syllog types and Syllogs
quants = np.array(['A', 'E', 'I', 'O', 'T', 'D'])
types = np.array(['u', 'u', 'e', 'e', 'g', 'g'])
syl_types = {}
for prem1, type1 in zip(quants, types):
    for prem2, type2 in zip(quants, types):
        for fig in ['1', '2', '3', '4']:
            syl_types[prem1 + prem2 + fig] = type1 + type2

# Annotate dataset with validity and correctness
data_df["valid"] = data_df["enc_task"].apply(lambda x: x in valid_syls)
data_df["correct"] = data_df[["enc_task", "enc_response"]].apply(lambda x: x["enc_response"] in cc[x["enc_task"]], axis=1)

# Annotate with genQuant information
data_df["is_genQuant"] = data_df["enc_task"].apply(lambda x: "T" in x or "D" in x)
data_df["syl_type"] = data_df["enc_task"].apply(lambda x: syl_types[x])
by_syllog = data_df.groupby("enc_task")[["enc_task", "correct", "is_genQuant", "valid"]].agg("mean").sort_values(by="correct", ascending=False)

# Define ordering, labels and colors
order = ["uu", "ue", "ee", "ug", "ge", "gg"]
labels = ["Universal", "Universal + \n Existential", "Existential", "Universal + \n Generalized", "Existential + \n Generalized", "Generalized"]
colors = ["C0", "C0", "C0", "C1", "C1", "C1"]

plt.figure(figsize=(6,4))
sns.set_theme(style="whitegrid", palette="colorblind")
ax = sns.barplot(x="syl_type", y="correct", data=data_df, order=order, palette=colors)
plt.ylim(0, 0.6)

sns.despine()

# Legend specification
lels = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='C0', markersize=10, label='Traditional Syllogisms'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='C1', markersize=10, label='Generalized Syllogisms'),
]
plt.legend(
    handles=lels, bbox_to_anchor=(0., 1.02, 1., .102), loc='center', ncol=2, borderaxespad=0.,
    frameon=False
)

plt.xlabel("")
ax.set_xticklabels(labels)
plt.ylabel("Correctness")

plt.tight_layout()
plt.savefig("Correctness_by_syl_type.pdf")
plt.show()

# Quartiles plot: Generating the quartiles
task_tuples = [{"Task" : task, "Correctness" : correct, "GenQuant" : is_genQuant, "Validity" : valid} for task, correct, is_genQuant, valid in by_syllog.itertuples()]
task_tuples_df = pd.DataFrame(task_tuples)

quartiles = [-1] + task_tuples_df["Correctness"].quantile([.25, .5, .75]).tolist() + [float("inf")]
task_tuples_df["quartiles"] = pd.cut(task_tuples_df["Correctness"], bins=quartiles, labels=["1st", "2nd", "3rd", "4th"])
quartiles_tasks = task_tuples_df.groupby("quartiles").agg("mean")

quartile_data = []
for row in quartiles_tasks.itertuples():
    name = row.Index
    correctness = row.Correctness
    genQuant = row.GenQuant
    validity = row.Validity
    quartile_data.append({
        "Quartile" : name,
        "Type" : "Correctness",
        "Proportion" : correctness
    })
    quartile_data.append({
        "Quartile" : name,
        "Type" : "GenQuant",
        "Proportion" : genQuant
    })
    quartile_data.append({
        "Quartile" : name,
        "Type" : "Validity",
        "Proportion" : validity
    })
quartile_data_df = pd.DataFrame(quartile_data)    

# plotting quartile barplots
order=["1st", "2nd", "3rd", "4th"]
hue_order = ["Correctness", "GenQuant", "Validity"]

plt.figure(figsize=(6,4))
sns.set_theme(style="whitegrid", palette="colorblind")
ax = sns.barplot(x="Quartile", y="Proportion", hue="Type", data=quartile_data_df, order=order, hue_order=hue_order)

plt.legend(frameon=False, ncol=3, loc='upper left', bbox_to_anchor=(0, 0.1, 1, 1))

plt.xlabel("Quartile by Correctness")
plt.ylabel("Proportion")
plt.ylim(0, 0.7)

plt.tight_layout()
plt.savefig("Quartiles.pdf")
plt.show()