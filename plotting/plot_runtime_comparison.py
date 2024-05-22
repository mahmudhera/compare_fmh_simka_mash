"""
sourmash_frackmc_comparison.csv contains the following columns:
filesize, avg_sourmash_time, std_sourmash_time, avg_frackmc_time, std_frackmc_time
We will plot the running time comparison of sourmash and frackmc sketch againts the filesize.
"""

import pandas as pd
import matplotlib.pyplot as plt

simka_color = '#377eb8'
mash_color = '#ff7f00'
frackmc_color = '#99DC97'
sourmash_color = '#9E4B9B'

df = pd.read_csv("sourmash_frackmc_comparison.csv")

# use ggplot style
#plt.style.use('seaborn-muted')

# use aptos font
plt.rcParams["font.family"] = "Arial"

# plot using side by side barplot, use colorblind friendly colors

palette = plt.get_cmap('gray')

fig, ax = plt.subplots()
bar_width = 0.22
index = df["filesize"]
bar3 = ax.bar(index - bar_width, df["avg_mash_time"], bar_width, label="mash sketch", color=mash_color, edgecolor='black')
bar1 = ax.bar(index, df["avg_sourmash_time"], bar_width, label="sourmash sketch", color=sourmash_color, edgecolor='black')
bar2 = ax.bar(index + bar_width, df["avg_frackmc_time"], bar_width, label="frac-kmc sketch", color=frackmc_color, edgecolor='black')


# add grid
ax.grid(axis="y")

# add error bars
ax.errorbar(index - bar_width, df["avg_mash_time"], yerr=df["std_mash_time"], fmt='none', ecolor="black")
ax.errorbar(index, df["avg_sourmash_time"], yerr=df["std_sourmash_time"], fmt='none', ecolor="black")
ax.errorbar(index + bar_width, df["avg_frackmc_time"], yerr=df["std_frackmc_time"], fmt='none', ecolor="black")


# add labels
ax.set_xlabel("Filesize (GB)")

# add y-axis label
ax.set_ylabel("Time (s)")

# add title
#ax.set_title("Running time comparison of sourmash sketch and FrackMC Sketch")

# add legend
ax.legend()

#plt.show()

# save the plot
plt.savefig("sourmash_frackmc_comparison.pdf", bbox_inches="tight")
#plt.close()