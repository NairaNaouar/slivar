import pandas as pd
import seaborn as sns

from matplotlib import rc

rc('font',**{'family':'sans-serif','sans-serif':['Arial']})


from matplotlib import pyplot as plt

import sys

colors = sns.color_palette("Set1", 12)

c = 0.5
colors = [(c, c, c), (c, c, c)]

args = sys.argv[1:][:]
assert len(sys.argv) == 5

# order is [GATK, DV, GATK-noLCR, DV-noLCR]
args[0] = [x for x in sys.argv[1:] if not "noLCR" in x and not 'dv' in x][0]
args[1] = [x for x in sys.argv[1:] if not "noLCR" in x and 'dv' in x][0]
args[2] = [x for x in sys.argv[1:] if "noLCR" in x and not 'dv' in x][0]
args[3] = [x for x in sys.argv[1:] if "noLCR" in x and 'dv' in x][0]

dfos = [pd.read_csv(arg, sep="\t", index_col=0).drop(["dn_ab_gq"], axis=1) for arg in args]

dfs = [dfo.melt(value_name="number_of_variants", id_vars=("dn_impactful",)) for dfo in dfos]

dfs = [[dfs[0], dfs[1]], [dfs[2], dfs[3]]]


fig, axes = plt.subplots(2, 2, figsize=(7, 7), sharey=True)


for i in range(0, 2):
    for j in range(0, 2):
        df = dfs[i][j]

        sns.boxplot(x="variable", y="number_of_variants",
               data=df, ax=axes[i, j], palette=colors) #, s=3)


axes[0,0].set_title("GATK", size=15)
axes[0,1].set_title("DeepVariant", size=15)
axes[1,0].set_title("GATK excluding LCR", size=15)
axes[1,1].set_title("DeepVariant excluding LCR", size=15)

axes[0,0].set_xlabel(None, size=15)
axes[0,1].set_xlabel(None, size=15)
axes[1,0].set_xlabel(None, size=15)
axes[1,1].set_xlabel(None, size=15)

axes[0,0].set_ylabel("Candidate $\it{de novo}$ variants")
axes[1,0].set_ylabel("Candidate $\it{de novo}$ variants")
axes[0,1].set_ylabel(None)
axes[1,1].set_ylabel(None)

xlabels = ["AB in 0.2..0.8\nGQ >= {cutoff}\nAF < 0.01",
           "AF < 0.001",
           "Absent/PASS\nin gnomAD"]

axes[0, 0].set_xticklabels([])


axes[1, 0].set_xticklabels([x.format(cutoff=20) for x in xlabels], rotation=12, ha="center")
axes[1, 1].set_xticklabels([x.format(cutoff=15) for x in xlabels], rotation=12, ha="center")
axes[0, 0].set_xticklabels([])
axes[0, 1].set_xticklabels([])



#axes[0,0].set_xticklabels(["0.2 <= AB < 0.8\n& GQ >= 20",
#                         "gnomAD popmax AF < 0.001\n& not non-PASS in gnomAD",
#                         "impactful"])

#axes[0].set_yticks(range(11))

#print(axes[0].get_xlim())

ax = axes[0, 0]
#ax.set_ylim(-0.5, 2000)
#ax.axhline(o, 0.1, 0.4, lw=4)
#ax.axhline(f, 1-0.4, 1 - 0.1, lw=4)

sns.despine()
plt.tight_layout()
plt.savefig("figure5-genome-denovos.png")
plt.show()




