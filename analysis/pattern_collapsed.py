import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import ccobra

# Load dataset
data = pd.read_csv("../data/Ragni2021.csv")

# Quantifiers and the respective types
quants = np.array(['A', 'E', 'I', 'O', 'T', 'D'])
types = np.array(['u', 'u', 'e', 'e', 'g', 'g'])

# Collapse across orders of premises and figures
SYLLOGISMS_collapsed = []
syl_type_collapsed = []
for prem1, type1 in zip(quants, types):
    for prem2, type2 in zip(quants[np.where(quants == prem1)[0][0]:], types[np.where(quants == prem1)[0][0]:]):
            SYLLOGISMS_collapsed.append(prem1 + prem2)
            syl_type_collapsed.append(type1 + type2)
SYLLOGISMS_collapsed = [x for _, x in sorted(zip(syl_type_collapsed, SYLLOGISMS_collapsed), reverse=True)]

# Collapse across orders of premises
RESPONSES_collapsed = []
resp_type_collapsed = []
for quant, quant_type in zip(quants, types):
        RESPONSES_collapsed.append(quant)
        resp_type_collapsed.append(quant_type)
RESPONSES_collapsed = [x for _, x in sorted(zip(resp_type_collapsed, RESPONSES_collapsed), reverse=True)]
RESPONSES_collapsed.append('NVC')
resp_type_collapsed.append(None)

pattern_collapsed = np.zeros((31, 21, 7))
pps = np.unique(data['id'])
for pp_i, pp in enumerate(pps):
    subject_data = data.loc[data['id'] == pp, ['enc_task', 'enc_response']]
    subject_data = subject_data.reset_index(drop=True)
    for task in range(len(subject_data)):
        try:
            task_i = SYLLOGISMS_collapsed.index(subject_data.loc[task, 'enc_task'][:2])
        except:
            task_i = SYLLOGISMS_collapsed.index(subject_data.loc[task, 'enc_task'][:2][::-1])
        try:
            response_i = RESPONSES_collapsed.index(subject_data.loc[task, 'enc_response'][0])
        except:
            response_i = RESPONSES_collapsed.index(subject_data.loc[task, 'enc_response'])
        pattern_collapsed[pp_i, task_i, response_i] += 1

# Normalize to account for the fact that syllogisms with different quantifiers are twice as often
pattern_collapsed_sum = pattern_collapsed.sum(axis=0)
pattern_collapsed_norm = pattern_collapsed_sum / pattern_collapsed_sum.sum(axis=1)[:, np.newaxis]

plt.figure(figsize=(6,6.5))
f1 = sns.heatmap(pattern_collapsed_norm, cmap='Blues', cbar=False, linewidths=0.8, linecolor='#00000025')
plt.yticks(ticks=np.arange(21)+.5,labels=np.array(SYLLOGISMS_collapsed),fontsize=13, rotation=0, va="center")
f1.set_xticklabels(RESPONSES_collapsed, fontsize=13)
plt.plot([0,7], [3,3], linewidth=3, color='black')
plt.plot([0,7], [7,7], linewidth=3, color='black')
plt.plot([0,7], [11,11], linewidth=3, color='black')
plt.plot([0,7], [14,14], linewidth=3, color='black')
plt.plot([0,7], [18,18], linewidth=3, color='black')
plt.plot([2,2], [0,21], linewidth=3, color='black')
plt.plot([4,4], [0,21], linewidth=3, color='black')
plt.plot([6,6], [0,21], linewidth=3, color='black')
ax2 = f1.secondary_yaxis('right')
ax2.set_yticks(ticks=np.array([1.5,5,9,12.5,16,19.5]))
ax2.set_yticklabels(['U', 'UG', 'UE', 'G', 'GE', 'E'], fontsize=17)
ax3 = f1.secondary_xaxis('top')
ax3.set_xticks(ticks=np.array([1,3,5]))
ax3.set_xticklabels(['U', 'G', 'E'], fontsize=17)

plt.tight_layout
plt.savefig("pattern_collapsed.pdf")
plt.show()