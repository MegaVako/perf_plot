import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

RECORD_IDX = 208
INPUT_FILE1 = "mem_koff_core.csv"
INPUT_FILE2 = "mem_kon_core.csv"

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
columns = ["Time", "SYSTEM_INST", "SYSTEM_CYCLE", "SYSTEM_REF_CYCLE"]
df1 = pd.read_csv(INPUT_FILE1, usecols=columns)
df2 = pd.read_csv(INPUT_FILE2, usecols=columns)

seq_int1 = np.linspace(0, int(len(df1.Time) / 2), len(df1.Time))
seq_int2 = np.linspace(0, int(len(df2.Time) / 2), len(df2.Time))

fig, ax = plt.subplots()
ax.plot(seq_int1, df1.SYSTEM_REF_CYCLE)
ax.plot(seq_int2, df2.SYSTEM_REF_CYCLE)
plt.xlabel('Time (seconds)')
plt.ylabel('Cycle')
plt.title("x86 Cycle vs. Time (sec)")
plt.legend(["ksm_ff", "ksm_on_at_x_time"])
plt.show()
