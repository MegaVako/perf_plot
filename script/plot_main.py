from matplotlib import pyplot as plt
import sys
from plot_perf import *

PLOT_ZSWAP = False
PLOT_LATS = False
PLOT_CACHE = True
PLOT_CYCLE = False
PLOT_KSWAP = False
PLOT_YCSB = True

plot_resolution = 0 # digit
#time_str = "14_36_36" # time sample in hpca_perf/data/
#time_str = "11_03_41" # l2
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
    #main_str = "Latency, L1d miss ratio @ Core {0} vs. Time (sec)".format(core_num)
    '''
    parse_files = [
        "../data/{0}/{0}_perf_L1-dcache-load-misses_perf.csv".format(time_str),
        "../data/{0}/{0}_perf_L1-dcache-loads_perf.csv".format(time_str),
    ]
    parse_files = [
        "../data/{0}/{0}_perf_l2_rqsts.miss_perf.csv".format(time_str),
        "../data/{0}/{0}_perf_l2_rqsts.references_perf.csv".format(time_str),
    ]
    '''
    main_str = "Latency, LLC miss ratio @ Core {0} vs. Time (sec)".format(core_num)
    parse_files = [
        "../data/{0}/{0}_perf_LLC-load-misses_perf.csv".format(time_str),
        "../data/{0}/{0}_perf_LLC-loads_perf.csv".format(time_str),
    ]
    graph_csv_area_ratio(parse_files, core_num, plot_resolution, plot_all=0, target_str="kswapd", ax=ax, ylab="LLC miss ratio")

# plot cycle
elif PLOT_CYCLE:
    #main_str = "Latency, CPU cycle @ Core {0} vs. Time (sec)".format(core_num)
    main_str = "CPU cycle @ Core {0} vs. Time (sec)".format(core_num)
    parse_files = [
        "../data/{0}/{0}_perf_cycles_perf.csv".format(time_str),
    ]
    parse_job(parse_files[0])
    graph_csv_area(parse_files, core_num, plot_resolution, plot_all=2, target_str="kswap", ax=ax)

# 14.9 is a manual shift added to the lat plot
if PLOT_LATS:
    graph_lats("../data/{0}/{1}_lats.csv".format(time_str, core_num), ax2, 14.9)

if PLOT_ZSWAP:
    graph_zswap("../data/{0}/{0}_mem_stat.csv".format(time_str), ax2)

if PLOT_KSWAP:
    #graph_kswapd_mem("../data/{0}/{0}_kswapd_mem.csv".format(time_str), ax2)
    graph_kswapd_mem("../data/{0}/{0}_kswapd_mem.csv".format(time_str), ax)

if PLOT_YCSB:
    graph_ycsb_lats("../data/{0}/{0}_ycsb_lat.csv".format(time_str), ax2, 9)

ax.legend(loc='upper left')
ax2.legend(loc='upper right')

ax.set_xlabel(x_lab_str)
plt.title(main_str)
plt.show()
