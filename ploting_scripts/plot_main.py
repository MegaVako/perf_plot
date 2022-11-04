from matplotlib import pyplot as plt
import sys
from plot_perf import *

PLOT_CACHE = False
PLOT_CYCLE = True

plot_resolution = 1 # digit
time_str = "08_10_13" # llc
x_lab_str = 'Time (seconds)'
main_str = ""
core_num = 14

if len(sys.argv) >= 2:
    time_str = sys.argv[1]
if len(sys.argv) >= 3:
    core_num = int(sys.argv[2])

fig, ax = plt.subplots()
ax2 = ax.twinx()

# plot cache
if PLOT_CACHE:
    main_str = "Latency, LLC miss ratio @ Core {0} vs. Time (sec)".format(core_num)
    parse_files = [
        "../results/{0}/{0}_perf_LLC-load-misses_perf.csv".format(time_str),
        "../results/{0}/{0}_perf_LLC-loads_perf.csv".format(time_str),
    ]
    graph_csv_area_ratio(parse_files, core_num, plot_resolution, plot_all=0, target_str="kswapd", ax=ax, ylab="LLC miss ratio")

# plot cycle
elif PLOT_CYCLE:
    #main_str = "Latency, CPU cycle @ Core {0} vs. Time (sec)".format(core_num)
    main_str = "CPU cycle @ Core {0} vs. Time (sec)".format(core_num)
    parse_files = [
        "../results/{0}/{0}_perf_cycles_perf.csv".format(time_str),
    ]
    #parse_job(parse_files[0])
    graph_csv_area(parse_files, core_num, plot_resolution, plot_all=0, target_str="kswap", ax=ax)

ax.legend(loc='upper left')
ax2.legend(loc='upper right')

ax.set_xlabel(x_lab_str)
plt.title(main_str)
plt.show()
