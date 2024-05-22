"""
In this script, we plot the results.
"""


import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
import seaborn as sns
import matplotlib.patches as mpatches


simka_color = '#377eb8'
mash_color = '#ff7f00'
frackmc_color = '#99DC97'


def plot1():
    data_used = data_wall_time
    labels = list(data_used.keys())
    values = np.array([list(map(lambda x: x if x is not None else np.nan, times)) for times in data_used.values()])

    # X locations for the groups
    x = np.arange(len(labels))

    # Bar width
    width = 0.22

    fontsize = 10
    plt.rc('font', size=fontsize)          # controls default text sizes

    fig, ax = plt.subplots(figsize=(5,3))

    # use arial font
    plt.rcParams['font.sans-serif'] = 'Arial'

    legends = ['Simka', 'Mash', 'Frac-KMC']
    hatch_style = ['xx', '..', '//']

    # Plotting each set of bars
    for i in range(values.shape[1]):
        ax.bar(x + i * width, values[:, i], width, label=legends[i], color=['white'], edgecolor=['black'], hatch=hatch_style[i])
        # Add large X markers for missing values
        for j, val in enumerate(values[:, i]):
            if np.isnan(val):
                ax.text(x[j] + i * width, 0, 'X', ha='center', va='bottom', color='red', fontsize=20)

    # Adding labels, title, and legend
    #ax.set_xlabel('Dataset')
    ax.set_ylabel('Time (seconds)')
    ax.set_xticks(x + width)
    ax.set_xticklabels(labels)
    ax.legend()

    # Display the plot
    plt.show()


def plot2():
    data_used = data_cpu_time
    labels = list(data_used.keys())
    values = np.array([list(map(lambda x: x if x is not None else np.nan, times)) for times in data_used.values()])

    # X locations for the groups
    x = np.arange(len(labels))

    # Bar width
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting each set of bars
    for i in range(values.shape[1]):
        ax.bar(x + i * width, values[:, i], width, label=f'Time {i + 1}')
        # Add large X markers for missing values
        for j, val in enumerate(values[:, i]):
            if np.isnan(val):
                ax.text(x[j] + i * width, 0, 'X', fontsize=20, ha='center', va='bottom', color='red')

    # Adding labels, title, and legend
    ax.set_xlabel('Dataset')
    ax.set_ylabel('Wall Time (s)')
    ax.set_title('Wall Time by Dataset and Time Interval')
    ax.set_xticks(x + width)
    ax.set_xticklabels(labels)
    ax.legend()

    # Display the plot
    plt.show()


def plot_actual_errors_hmp(ax):
    df = pd.read_csv("hmp_combined", delim_whitespace=True)
    mash_cosine_ecoli = df['mash'].tolist()
    frackmc_cosine_ecoli = df['fmh'].tolist()
    true_cosine_ecoli = df['gt'].tolist()

    # show a line y = x
    ax.plot([0, 1], [0, 1], color='grey', linestyle='--', linewidth=1)

    # plot mash and frackmc ecoli values againts the true values in a scatter plot
    ax.scatter(true_cosine_ecoli, mash_cosine_ecoli, label='Mash', color=mash_color, alpha=0.45, marker='s')
    ax.scatter(true_cosine_ecoli, frackmc_cosine_ecoli, label='frac-kmc', color=frackmc_color, alpha=0.45, marker='o')

    # add labels
    ax.set_xlabel("True Cosine (HMP)")
    ax.set_ylabel("Estimated Cosine (HMP)")

    # add legend
    ax.legend()

    # flip order of legends
    handles, labels = ax.get_legend_handles_labels()
    #ax.legend(handles[::-1], labels[::-1])

    # set legend's alpha=1
    for lh in ax.legend().legendHandles:
        lh.set_alpha(1)

    # tight layout
    plt.tight_layout()

    # add legend
    mash_patch = mpatches.Patch(facecolor=mash_color, label='Mash')
    frackmc_patch = mpatches.Patch(facecolor=frackmc_color, label='frac-kmc')
    ax.legend(handles=[frackmc_patch, mash_patch])

    #plt.show()



def plot_actual_errors_ecoli(ax):
    df = pd.read_csv("ecoli_combined", delim_whitespace=True)
    mash_cosine_ecoli = df['mash'].tolist()
    frackmc_cosine_ecoli = df['fmh'].tolist()
    true_cosine_ecoli = df['gt'].tolist()

    #fig, ax = plt.subplots()

    # show a line y = x
    ax.plot([0, 1], [0, 1], color='grey', linestyle='--', linewidth=1)

    # plot mash and frackmc ecoli values againts the true values in a scatter plot
    ax.scatter(true_cosine_ecoli, mash_cosine_ecoli, label='Mash', color=mash_color, alpha=0.45, marker='s')    
    ax.scatter(true_cosine_ecoli, frackmc_cosine_ecoli, label='frac-kmc', color=frackmc_color, alpha=0.45, marker='o')

    # add labels
    ax.set_xlabel("True Cosine (Ecoli)")
    ax.set_ylabel("Estimated Cosine (Ecoli)")

    # add legend
    ax.legend()

    # flip order of legends
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])

    # set legend's alpha=1
    for lh in ax.legend().legendHandles:
        lh.set_alpha(1)

    # add legend
    mash_patch = mpatches.Patch(facecolor=mash_color, label='Mash')
    frackmc_patch = mpatches.Patch(facecolor=frackmc_color, label='frac-kmc')
    ax.legend(handles=[frackmc_patch, mash_patch])

    # tight layout
    plt.tight_layout()

    #plt.show()



def plot_violins(ax):
    df = pd.read_csv("ecoli_combined", delim_whitespace=True)
    errors_mash_ecoli = df['mash_error'].tolist()
    errors_frackmc_ecoli = df['fmh_error'].tolist()
    true_cosine = df['gt'].tolist()

    errors_mash_ecoli_pctg = [ 100*x/t for x, t in zip(errors_mash_ecoli, true_cosine) ]
    errors_frackmc_ecoli_pctg = [ 100*x/t for x, t in zip(errors_frackmc_ecoli, true_cosine) ]

    df = pd.read_csv("hmp_combined", delim_whitespace=True)
    errors_mash_hmp = df['mash_error'].tolist()
    errors_frackmc_hmp = df['fmh_error'].tolist()
    true_cosine = df['gt'].tolist()

    errors_mash_hmp_pctg = [ 100*x/t for x, t in zip(errors_mash_hmp, true_cosine) ]
    errors_frackmc_hmp_pctg = [ 100*x/t for x, t in zip(errors_frackmc_hmp, true_cosine) ]

    datasets = ['Ecoli', 'HMP']

    # Plotting
    #fig, ax = plt.subplots()
    

    #bplot1 = plt.boxplot([errors_mash_ecoli_pctg, errors_frackmc_ecoli_pctg], labels=['Mash', 'FrackMC'], notch=True, patch_artist=True, positions=[0.9, 1.1], showfliers=False)
    vplot1 = ax.violinplot([errors_mash_ecoli_pctg, errors_frackmc_ecoli_pctg], positions=[0.9, 1.1], showextrema=False, showmedians=False, widths=0.25)
    #bplot2 = plt.boxplot([errors_mash_hmp_pctg, errors_frackmc_hmp_pctg], labels=['Mash', 'FrackMC'], notch=True, patch_artist=True, positions=[1.4, 1.6], showfliers=False)
    vplot2 = ax.violinplot([errors_mash_hmp_pctg, errors_frackmc_hmp_pctg], positions=[1.9, 2.1], showextrema=False, showmedians=False, widths=0.25)

    colors = [mash_color, frackmc_color, mash_color, frackmc_color]

    i = 0
    for patch in vplot1['bodies'] + vplot2['bodies']:
        patch.set_facecolor(colors[i])
        if i % 2 == 0:
            patch.set_alpha(0.99)
        else:
            patch.set_alpha(1)
        i += 1

    colors2 = ['bisque', 'lightgreen']
    #vplot1['cmedians'].set_colors(colors2)
    #vplot2['cmedians'].set_colors(colors2)

    # add labels
    ax.set_xticks([1, 2])
    ax.set_xticklabels(datasets)

    # add legend
    mash_patch = mpatches.Patch(facecolor=mash_color, label='Mash')
    frackmc_patch = mpatches.Patch(facecolor=frackmc_color, label='frac-kmc')
    ax.legend(handles=[frackmc_patch, mash_patch], loc='lower center')

    # add y-axis label
    ax.set_ylabel("Error (%)")

    # show y grid
    #ax.grid(axis="y")


def plot_ecoli_cputime_large(ax):
    #fig, ax = plt.subplots()

    df = pd.read_csv("ecoli_runtime")
    df = df[df["num_files"] >= 1000]

    mash_times = df[df["method"] == "mash"]["cputime"].tolist()
    frackmc_times = df[df["method"] == "frackmc"]["cputime"].tolist()

    bar_width = 120

    index = df['num_files'].tolist()[ :len(df['num_files'].tolist())//2 ]
    index = np.array(index)
    

    # show times for frac-kmc
    ax.plot(index, frackmc_times, label="frac-kmc", color=frackmc_color, marker = 'o', markersize=7, linestyle='-')

    # show times for mash
    ax.plot(index, mash_times, label="Mash", color=mash_color, marker = 's', markersize=7, linestyle='-')

    # add grid
    ax.grid(axis="y")

    ax.set_xticks(index)
    ax.set_xticklabels(index)

    # add labels
    ax.set_xlabel("Num. samples")

    # add y-axis label
    ax.set_ylabel("CPU time (Ecoli, s)")

    # add legend
    ax.legend()

    # tight layout
    plt.tight_layout()

    #plt.show()


def plot_ecoli_walltime_large(ax):
    #fig, ax = plt.subplots()

    df = pd.read_csv("ecoli_runtime")
    df = df[df["num_files"] >= 1000]

    mash_times = df[df["method"] == "mash"]["walltime"].tolist()
    frackmc_times = df[df["method"] == "frackmc"]["walltime"].tolist()

    index = df['num_files'].tolist()[ :len(df['num_files'].tolist())//2 ]
    index = np.array(index)
    
    
    # show times for frac-kmc
    ax.plot(index, frackmc_times, label="frac-kmc", color=frackmc_color, marker = 'o', markersize=7, linestyle='-')

    # show times for mash
    ax.plot(index, mash_times, label="Mash", color=mash_color, marker = 's', markersize=7, linestyle='-')


    # add grid
    ax.grid(axis="y")

    ax.set_xticks(index)
    ax.set_xticklabels(index)

    # add labels
    ax.set_xlabel("Num. samples")

    # add y-axis label
    ax.set_ylabel("Wall-clock time (Ecoli, s)")

    # add legend
    ax.legend()
    #handles, labels = ax.get_legend_handles_labels()
    #ax.legend(handles[::-1], labels[::-1])

    # tight layout
    plt.tight_layout()

    #plt.show()


def plot_ecoli_walltime_small(ax):
    #fig, ax = plt.subplots()

    df = pd.read_csv("ecoli_runtime")
    df = df[df["num_files"] <= 125]

    mash_times = df[df["method"] == "mash"]["walltime"].tolist()
    simka_times = df[df["method"] == "simka"]["walltime"].tolist()
    frackmc_times = df[df["method"] == "frackmc"]["walltime"].tolist()

    bar_width = 6

    index = df['num_files'].tolist()[ :len(df['num_files'].tolist())//3 ]
    index = np.array(index)
    
    bar2 = ax.bar(index - bar_width, simka_times, bar_width, label="Simka", color=simka_color, edgecolor='black')
    bar3 = ax.bar(index, frackmc_times, bar_width, label="frac-kmc", color=frackmc_color, edgecolor='black')
    bar1 = ax.bar(index + bar_width, mash_times, bar_width, label="Mash", color=mash_color, edgecolor='black')
    

    # add grid
    ax.grid(axis="y")

    # write a letter X at 125
    ax.text(125-bar_width, 0, "X", fontsize=13, ha='center', va='bottom', color='red')

    ax.set_xticks(index)
    ax.set_xticklabels(index)

    # add labels
    ax.set_xlabel("Num. samples")

    # add y-axis label
    ax.set_ylabel("Wall-clock time (Ecoli, s)")

    # add legend
    ax.legend()

    # tight layout
    plt.tight_layout()

    #plt.show()


def plot_hmp_walltime_small(ax):
    #fig, ax = plt.subplots()

    df = pd.read_csv("hmp_gut_runtime")
    df = df[df["num_files"] <= 125]

    mash_times = df[df["method"] == "mash"]["walltime"].tolist()
    simka_times = df[df["method"] == "simka"]["walltime"].tolist()
    frackmc_times = df[df["method"] == "frackmc"]["walltime"].tolist()

    bar_width = 6

    index = df['num_files'].tolist()[ :len(df['num_files'].tolist())//3 ]
    index = np.array(index)
    
    bar2 = ax.bar(index - bar_width, simka_times, bar_width, label="Simka", color=simka_color, edgecolor='black')
    bar3 = ax.bar(index, frackmc_times, bar_width, label="frac-kmc", color=frackmc_color, edgecolor='black')
    bar1 = ax.bar(index + bar_width, mash_times, bar_width, label="Mash", color=mash_color, edgecolor='black')
    

    # add grid
    ax.grid(axis="y")

    # write a letter X at 125
    ax.text(125-bar_width, 0, "X", fontsize=13, ha='center', va='bottom', color='red')

    ax.set_xticks(index)
    ax.set_xticklabels(index)

    # add labels
    ax.set_xlabel("Num. samples")

    # add y-axis label
    ax.set_ylabel("Wall-clock time (HMP, s)")

    # add legend
    ax.legend()

    # tight layout
    plt.tight_layout()

    #plt.show()


def plot_hmp_walltime_large(ax):
    #fig, ax = plt.subplots()

    df = pd.read_csv("hmp_gut_runtime")

    file_sizes_to_show = [100, 150, 200, 250, 300]
    df = df[df["num_files"].isin(file_sizes_to_show)]

    file_size_to_mash_times = {}
    file_size_to_frackmc_times = {}

    for file_size in file_sizes_to_show:
        file_size_to_mash_times[file_size] = df[(df["method"] == "mash") & (df["num_files"] == file_size)]["walltime"].tolist()
        file_size_to_frackmc_times[file_size] = df[(df["method"] == "frackmc") & (df["num_files"] == file_size)]["walltime"].tolist()

    bar_width = 12

    index = np.array(file_sizes_to_show)
    mash_times = [ file_size_to_mash_times[file_size][0] for file_size in file_sizes_to_show ]
    frackmc_times = [ file_size_to_frackmc_times[file_size][0] for file_size in file_sizes_to_show ]
    
    
    # show times for frac-kmc
    ax.plot(index, frackmc_times, label="frac-kmc", color=frackmc_color, marker = 'o', markersize=7, linestyle='-')

    # show times for mash
    ax.plot(index, mash_times, label="Mash", color=mash_color, marker = 's', markersize=7, linestyle='-')

    # add grid
    ax.grid(axis="y")

    ax.set_xticks(index)
    ax.set_xticklabels(index)

    # add labels
    ax.set_xlabel("Num. samples")

    # add y-axis label
    ax.set_ylabel("Wall-clock time (HMP, s)")

    # add legend
    ax.legend()

    # tight layout
    plt.tight_layout()

    #plt.show()


def plot_hmp_cputime_large(ax):
    #fig, ax = plt.subplots()

    df = pd.read_csv("hmp_gut_runtime")

    file_sizes_to_show = [100, 150, 200, 250, 300]
    df = df[df["num_files"].isin(file_sizes_to_show)]

    file_size_to_mash_times = {}
    file_size_to_frackmc_times = {}

    for file_size in file_sizes_to_show:
        file_size_to_mash_times[file_size] = df[(df["method"] == "mash") & (df["num_files"] == file_size)]["cputime"].tolist()
        file_size_to_frackmc_times[file_size] = df[(df["method"] == "frackmc") & (df["num_files"] == file_size)]["cputime"].tolist()

    index = np.array(file_sizes_to_show)
    mash_times = [ file_size_to_mash_times[file_size][0] for file_size in file_sizes_to_show ]
    frackmc_times = [ file_size_to_frackmc_times[file_size][0] for file_size in file_sizes_to_show ]

    # show times for frac-kmc
    ax.plot(index, frackmc_times, label="frac-kmc", color=frackmc_color, marker = 'o', markersize=7, linestyle='-')

    # show times for mash
    ax.plot(index, mash_times, label="Mash", color=mash_color, marker = 's', markersize=7, linestyle='-')

    # add grid
    ax.grid(axis="y")

    ax.set_xticks(index)
    ax.set_xticklabels(index)

    # add labels
    ax.set_xlabel("Num. samples")

    # add y-axis label
    ax.set_ylabel("CPU time (HMP, s)")

    # add legend
    ax.legend()

    # tight layout
    plt.tight_layout()

    #plt.show()



if __name__ == "__main__":
    # use aptos font
    plt.rcParams["font.family"] = "Arial"

    # set font size to 10
    plt.rcParams.update({'font.size': 10})

    # 3x3 plot
    fig, axs = plt.subplots(3, 3, figsize=(9, 6))

    # use ggplot style
    #plt.style.use('ggplot')

    plot_ecoli_walltime_small(axs[0, 0])
    plot_ecoli_walltime_large(axs[0, 1])
    plot_ecoli_cputime_large(axs[0, 2])
    plot_hmp_walltime_small(axs[1, 0])
    plot_hmp_walltime_large(axs[1, 1])
    plot_hmp_cputime_large(axs[1, 2])
    plot_violins(axs[2, 0])
    plot_actual_errors_ecoli(axs[2, 1])
    plot_actual_errors_hmp(axs[2, 2])

    plt.tight_layout()
    plt.savefig('all-comparisons.pdf')