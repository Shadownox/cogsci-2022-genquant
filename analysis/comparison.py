import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import ccobra

def gen_task_enc(elem):
    item = ccobra.Item(0, "syllogistic", elem, "single-choice", "", 0)
    syl = ccobra.syllogistic.Syllogism(item)
    return syl.encoded_task

def gen_resp_enc(elem):
    item = ccobra.Item(0, "syllogistic", elem["task"], "single-choice", "", 0)
    syl = ccobra.syllogistic.Syllogism(item)
    return syl.encode_response(elem["response"].split(";"))

responses =ccobra.syllogistic.RESPONSES + ["Tac", "Tca", "Dac", "Dca"]

def generate_matrix(df):
    mat = np.zeros((len(ccobra.syllogistic.SYLLOGISMS), len(responses)))
    num_people = len(np.unique(df["id"]))
    for _, row in df.iterrows():
        if "enc_task" not in row:
            print(row)
            exit()
        syl = row["enc_task"]
        resp = row["enc_response"]
        
        if syl in ccobra.syllogistic.SYLLOGISMS:
            syl_idx = ccobra.syllogistic.SYLLOGISMS.index(syl)
            resp_idx = responses.index(resp)
            mat[syl_idx, resp_idx] += 1/num_people
    return mat

# Load genquant dataset    
genquant_df = pd.read_csv("../data/Ragni2021.csv")

# Load ragni2016 dataset and add encodings
classic_df = pd.read_csv("../data/Ragni2016.csv")
classic_df["enc_task"] = classic_df["task"].apply(gen_task_enc)
classic_df["enc_response"] = classic_df[["task", "response"]].apply(gen_resp_enc, axis=1)

# Generate matrices for both
gen_mat = generate_matrix(genquant_df)
cla_mat = generate_matrix(classic_df)

# Calculate RMSE
rmses = []
for i in range(64):
    rmses.append(np.mean((gen_mat[i] - cla_mat[i])**2)**0.5)
    
print("RMSE:", np.mean(rmses))

# Plot matrices
fig, axs = plt.subplots(1, 2, figsize=(6, 8), sharey=True)
sns.set(style='darkgrid')

sns.heatmap(gen_mat, ax=axs[0], cmap='Blues', cbar=False, linewidths=0.5, linecolor='#00000022')
sns.heatmap(cla_mat, ax=axs[1], cmap='Blues', cbar=False, linewidths=0.5, linecolor='#00000022')

xticks = np.arange(0, len(responses), 1)
axs[0].set_xticks(xticks + 0.5)
axs[0].set_xticklabels([responses[x] for x in xticks], rotation=90)
axs[1].set_xticks(xticks + 0.5)
axs[1].set_xticklabels([responses[x] for x in xticks], rotation=90)

yticks = np.arange(0, len(ccobra.syllogistic.SYLLOGISMS), 4)
axs[0].set_yticks(yticks + 0.5)
axs[0].set_yticklabels([ccobra.syllogistic.SYLLOGISMS[x] for x in yticks], rotation=0)

axs[0].set_title("GenQuant Dataset")
axs[1].set_title("Traditional Dataset")
plt.tight_layout()

plt.savefig("Comparison.pdf")
plt.show()