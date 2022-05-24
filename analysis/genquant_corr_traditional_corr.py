import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats

from correct_conclusions import correct_conclusions as cc

data_df = pd.read_csv("../data/Ragni2021.csv")

# Annotate the dataset with additional information
data_df["is_genQuant"] = data_df["enc_task"].apply(lambda x: "T" in x or "D" in x)
data_df["correct"] = data_df[["enc_task", "enc_response"]].apply(lambda x: x["enc_response"] in cc[x["enc_task"]], axis=1)

# Group by participant
participants = data_df.groupby("id")

# For each participant, check correctness on genQuant and non-genQuant
results = []
for _id, part_df in participants:
    genQuants = part_df[part_df["is_genQuant"]]
    traditionals = part_df[~part_df["is_genQuant"]]
    
    gen_corr = genQuants["correct"].mean()
    trad_corr = traditionals["correct"].mean()
    
    results.append({
        "id" : _id,
        "genQuant" : gen_corr,
        "traditional" : trad_corr
    })
results = pd.DataFrame(results)

# Calculate spearman correlation
corr, p = stats.spearmanr(results["genQuant"], results["traditional"])
print("Spearman r={}, p={}".format(corr, p))

# Plot linear relationship and datapoints
sns.set_theme(style="whitegrid", palette="colorblind")
plt.figure(figsize=(5,3.5))
plt.scatter('traditional', 'genQuant', data=results, color="C0", marker='o', edgecolors="k")

# Fit linear regression via least squares
b, a = np.polyfit(results["traditional"], results["genQuant"], deg=1)

# X-values for the line
xseq = np.array([0, 1])

# Plot regression line
plt.plot(xseq, a + b * xseq, color="C0", lw=1.5, alpha=0.7);

# Style plot
plt.xlim(0.1, 0.7)
plt.ylim(0, 0.7)

plt.xlabel("Traditional Quantifiers")
plt.ylabel("Generalized Quantifiers")

plt.tight_layout()
plt.savefig("genquant_vs_traditional_correctness.pdf")
plt.show()

