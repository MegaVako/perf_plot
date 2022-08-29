import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

def annot_val(x_val, y_val, input_text, text_x, text_y, angleB, ax):
    text = input_text
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB={0}".format(angleB))
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="left", va="top")

    ax.annotate(text, xy=(x_val, y_val), xytext=(text_x, text_y), **kw)

plt.rcParams["figure.figsize"] = [15.00, 7.00]
plt.rcParams["figure.autolayout"] = True
columns = ["Time", "SYSTEM_L3MISS", "SYSTEM_L2MISS"]

for i in range(15): 
    columns.append("C{0}_L2MISS".format(i))
    columns.append("C{0}_L3MISS".format(i))

fig, ax = plt.subplots()

#gs = fig.add_gridspec(3, hspace=0)
#axs = gs.subplots(sharex=True, sharey=True)
legend_arr = []

def graph_df(df, file_name, seq_int, color, idx, plot_core):
    if plot_core:
        for i, col in enumerate(df.columns[5:]):
            if i % 2 == 1:
                continue
            legend_arr.append("{0} -- {1}".format(file_name, col))
            ax.plot(seq_int, df[col], color)
    else:
        col_name = df.columns[idx]
        legend_arr.append("{0} -- {1}".format(file_name, col_name))
        ax.plot(seq_int, df[col_name], color)

def graph_csv(file_name, color, head_n, idx, plot_core, do_anno, kon_idx, koff_idx):
    df = pd.read_csv(file_name, usecols=columns)
    
    #df = df.clip(upper=pd.Series({'SYSTEM_L3MISS': 15}), axis=1)
    df = df.head(head_n)

    seq_int = np.linspace(0, int(len(df.Time) / 2), len(df.Time))

    graph_df(df, file_name, seq_int, color, idx, plot_core)

    if (do_anno):
        annot_val(seq_int[kon_idx], df.SYSTEM_L2MISS[kon_idx], "ksm_on", 0.05, 0.94, "-60", ax)
        annot_val(seq_int[koff_idx], df.SYSTEM_L2MISS[koff_idx], "ksm_off", 0.3, 0.05, "60", ax)
        plt.axvline(seq_int[kon_idx], color="red", linestyle='--')
        plt.axvline(seq_int[koff_idx], color="red", linestyle='--')


plot_col_idx = 1
#graph_csv(INPUT_FILE1, "red", 1200, plot_col_idx, False, False, 0, 0)
#graph_csv(INPUT_FILE2, "green", 1200, plot_col_idx, False, False, 0, 0)
'''
graph_csv("zswap_fff_00.csv", "blue", 2000, plot_col_idx, False, False, 237, 483)
graph_csv("zswap_nnn_00.csv", "orange", 2000, plot_col_idx, False, False, 0, 0)
'''
graph_csv("./hpca/ksm_fff_02.csv", "blue", 2000, plot_col_idx, False, False, 237, 483)
graph_csv("./hpca/ksm_fnf_02.csv", "orange", 2000, plot_col_idx, False, True, 598, 962)

#graph_csv("./hpca/zswap100_fff_00.csv", "blue", 2000, plot_col_idx, False, False, 237, 483)
#graph_csv("./hpca/zswap100_nnn_00.csv", "red", 2000, plot_col_idx, False, False, 237, 483)
#graph_csv("./hpca/zswap100_nnn_01.csv", "green", 2000, plot_col_idx, False, False, 237, 483)
#graph_csv("./hpca/zswap100_nnn_02.csv", "black", 2000, plot_col_idx, False, False, 237, 483)
#graph_csv("./hpca/zswap500_nnn_00.csv", "black", 2000, plot_col_idx, False, False, 237, 483)
#graph_csv("./hpca/ksm_fff_00.csv", "orange", 2000, plot_col_idx, False, False, 237, 483)

'''
plot_col_idx = 2
graph_csv("zswap_fff_00.csv", "blue", 2000, plot_col_idx, False, False, 237, 483)
graph_csv("zswap_nnn_00.csv", "orange", 2000, plot_col_idx, False, False, 0, 0)
'''

'''
star_idx = [6, 7, 74, 75, 336, 337, 586, 587]
for idx in star_idx:
    ax.plot(seq_int3[idx], df3.SYSTEM_L3MISS[idx], 'r*')
'''

plt.xlabel('Time (seconds)')
plt.ylabel('LLC Miss Rate')
plt.title("LLC Miss Rate vs. Time (sec)")
plt.legend(legend_arr)
plt.show()
