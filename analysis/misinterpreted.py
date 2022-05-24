import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from correct_conclusions import correct_conclusions

data = pd.read_csv("../data/Ragni2021.csv")

# Replaces the generalized quantifiers by the traditional particular quantifiers
def replace_genquant(quant):
    if quant == "T":
        return "O"
    elif quant == "D":
        return "I"
    else:
        return quant

# Swaps the existential quantifiers
def replace_existquant(quant):
    if quant == "O":
        return "I"
    elif quant == "I":
        return "O"
    else:
        return quant

# Create mappings for possible misunderstandings: I <-> O, T -> O, D -> I
task_mapping_genquant = {}
task_mapping_existential = {}

for task in correct_conclusions.keys():
    if "T" in task or "D" in task:
        mis_task = replace_genquant(task[0]) + replace_genquant(task[1]) + task[2]
        task_mapping_genquant[task] = mis_task
    elif "I" in task or "O" in task:
        mis_task = replace_existquant(task[0]) + replace_existquant(task[1]) + task[2]
        task_mapping_existential[task] = mis_task

# Initialize result counters
results = {
    "Generalized" : {
        "correct": 0,
        "misinterpreted": 0,
        "incorrect": 0
    },
    "Existential" : {
        "correct": 0,
        "misinterpreted": 0,
        "incorrect": 0
    }
}

# Determine for each syllogism and response if it is
# 1) correct
# 2) correct if some/most are interpreted to exclude all
# 3) incorrect
for _, row in data.iterrows():
    task = row["enc_task"]
    correct_conc = correct_conclusions[task]
    resp = row["enc_response"]
    
    if task in task_mapping_genquant:
        if resp in correct_conc:
            results["Generalized"]["correct"] += 1
        elif resp in correct_conclusions[task_mapping_genquant[task]]:
            results["Generalized"]["misinterpreted"] += 1
        else:
            results["Generalized"]["incorrect"] += 1
    elif task in task_mapping_existential:
        if resp in correct_conc:
            results["Existential"]["correct"] += 1
        elif resp in correct_conclusions[task_mapping_existential[task]]:
            results["Existential"]["misinterpreted"] += 1
        else:
            results["Existential"]["incorrect"] += 1

# Aggregate in a dataframe
res = []
for typ in results.keys():
    total = 0
    
    for val in results[typ].values():
        total += val
    
    for cat in results[typ].keys():
        res.append({
            "Quantifier" : typ,
            "cat" : cat,
            "ratio" : results[typ][cat] / total
        })
plot_df = pd.DataFrame(res)

# Plot barplot
plt.figure(figsize=(5, 3.5))
sns.set_theme(style="whitegrid", palette="colorblind")
ax = sns.barplot(x="cat", y="ratio", hue="Quantifier", data=plot_df)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[0:], labels=labels[0:])

ax.set_xlabel("")
ax.set_ylabel("Proportion of responses")

plt.tight_layout()
plt.savefig("misinterpreted.pdf")
plt.show()

