import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

plt.rcParams["figure.figsize"] = [15.00, 7.00]
plt.rcParams["figure.autolayout"] = True
columns = ["time", "count", 'process', 'cpu', 'job', 'pid']
zswap_col = ['failed_stores','invalidates','loads','succ_stores','duplicate_entry','pool_limit_hit','pool_total_size','reject_alloc_fail','reject_compress_poor','reject_kmemcache_fail','reject_reclaim_fail','same_filled_pages','stored_pages','written_back_pages','mem_total','mem_used','mem_free','mem_shared','mem_buff/cache','mem_available','swap_total','swap_used','swap_free']
kswapd_col = ['record_id','ts','cmdline','stat_pid','stat_comm','stat_state','stat_ppid','stat_pgrp','stat_session','stat_tty_nr','stat_tpgid','stat_flags','stat_minflt','stat_cminflt','stat_majflt','stat_cmajflt','stat_utime','stat_stime','stat_cutime','stat_cstime','stat_priority','stat_nice','stat_num_threads','stat_itrealvalue','stat_starttime','stat_vsize','stat_rss']


def graph_group(group_df, group_name, color):
    legend_arr.append(group_name)
    ax.plot(group_df['time'], group_df['count'])

def graph_csv(file_name):
    df = pd.read_csv(file_name, usecols=columns)
    grouped = (df.groupby(['cpu', 'pid']))

    arr = []
    for core, proc in grouped.groups:
        if core != 14:
            continue
        curr_group = grouped.get_group((core, proc))
        color = 'green'
        print(proc)
        if 'ksm' in proc:
            color = 'red'
        elif 'KVM' in proc:
            color = 'blue'
        else:
            continue
        arr.append((proc, curr_group))
        #graph_group(curr_group, proc, color)

    for idx in range(len(arr)):
        rev_idx = len(arr) - idx -21
        print(arr[rev_idx])
        graph_group(arr[rev_idx][1], arr[rev_idx][0], "red")

def parse_data(file_name, core_num, round_factor, plot_all, target_str):
    df = pd.read_csv(file_name, usecols=columns)
    time_min = df['time'].min()
    df['time'] = df['time'].apply(lambda x: x-time_min)
    df['time'] = df['time'].round(round_factor) 

    df = df.rename(columns={"count": "e_count"})

    grouped = (df.groupby(['cpu']))
    for core in grouped.groups:
        if core == core_num:
            df = grouped.get_group(core)
            break

    grouped = df.groupby(['time', 'pid'])

    df = pd.DataFrame([{'time': pair[0],
                        'e_count': v.e_count.sum(),
                        'pid': pair[1]} 
                        for pair, v in grouped], 
                        columns=['time', 'e_count', 'pid'])

    cnt = 0
    t_min = 0
    t_max = df.time.max()
    sample_step = (10**(-round_factor))
    new_index = np.arange(t_min, t_max+1, sample_step)
    new_index = np.round(new_index, round_factor)
    df2 = pd.DataFrame(index=new_index)

    for proc, v in df.groupby(['pid']):
        if plot_all == 0: # ksm only
            if not (target_str in proc or 
                    "KVM" in proc):
            #if not ("KVM" in proc):
                continue
        elif plot_all == 1: # without ksm
            if (target_str in proc or 
                "KVM" in proc):
                continue

        # 
        #v['time'] = v['time'].round(round_factor)
        v = v.set_index('time')
        v = v.reindex(new_index, fill_value=0)

        df2.insert(cnt, proc, v['e_count'].astype(int))
        cnt += 1

    df2 = df2.fillna(0)
    print(df2.index.inferred_type)
    print(df2)
    return df2

def graph_csv_area_ratio(file_name, core_num, round_factor, plot_all, target_str, ax, ylab):
    df_miss = parse_data(file_name[0], core_num, round_factor, plot_all, target_str)
    df_load = parse_data(file_name[1], core_num, round_factor, plot_all, target_str)

    '''
    df_miss.plot(kind='area', linewidth=0)
    df_load.plot(kind='area', linewidth=0)
    '''
    
    # time, proc_1_miss, proc_2_miss ....
    df_ratio = df_miss.div(df_load)
    #df_ratio.plot(kind='area', linewidth=0, stacked=False, ax=ax)
    df_ratio.plot(kind='area', linewidth=0, ax=ax)
    ax.set_ylabel(ylab)

    #print(df2.to_string())
    #df2.plot(kind='area', linewidth=0)
    
def graph_csv_area(file_name, core_num, round_factor, plot_all, target_str, ax):
    ax.legend(loc="upper left")
    df = parse_data(file_name[0], core_num, round_factor, plot_all, target_str)
    df.plot(use_index=True, kind='area', linewidth=0, ax=ax, ylim=(0, 1.2*(10**8)))
    ax.set_ylabel('cycle')
    #df.plot(kind='area', linewidth=0, ylim=(0, 4*(10**8)), ax=ax)
    #df.plot(kind='area', linewidth=0, ylim=(0, 3*(10**8)))

def graph_zswap(file_name, ax):
    ax.set_ylabel("stored pages detla")
    ax.legend(loc=2)

    df = pd.read_csv(file_name, usecols=zswap_col)
    df_len = len(df)
    df['time'] = np.linspace(0, df_len/10, num=df_len).tolist()
    df = df.set_index('time')
    
    for column in df:
        curr_min = df[column].min()
        df[column] = df[column].apply(lambda x: x-curr_min)

    df['delta'] = df.stored_pages.diff().shift(-1)
    print(df.index.inferred_type)
    print(df)
    df.plot(use_index=True, y=['delta'], kind='line', ax=ax, color='b')

def graph_lats(file_name, ax, offset_t):

    ax.set_ylabel("sojourn time (us)")
    df = pd.read_csv(file_name, names=['sojourn_t'])
    df_len = len(df)
    df['time'] = np.linspace(offset_t, (df_len/2000) + offset_t, num=df_len).tolist()
    df = df.set_index('time')

    print(df.index.inferred_type)
    df.plot(use_index=True, y=['sojourn_t'], kind='line', ax=ax, color='r')

def graph_kswapd_mem(file_name, ax):
    ax.set_ylabel("Resident Set(MiB)")
    df = pd.read_csv(file_name, usecols=kswapd_col)

    ts_min = df['ts'].min()
    df['time'] =  df['ts'].apply(lambda x : x - ts_min)
    df = df.set_index('time')

    print(df.index.inferred_type)
    #df.plot(use_index=True, y=['stat_rss'], kind='line', ax=ax, color='g')
    df.plot(use_index=True, y=['stat_stime'], kind='line', ax=ax, color='g')
    
def graph_ycsb_lats(file_name, ax, offset_t):
    df = pd.read_csv(file_name, names=['op', 'ts', 'lats'])

    df['time'] =  df['ts'].apply(lambda x : x / 1000)
    ts_min = df['time'].min()
    ts_min -= offset_t
    df['time'] =  df['time'].apply(lambda x : x - ts_min)
    df = df.sort_values('time')
    df['ts'] = df['time']
    df = df.set_index('time')

    print(df.index.inferred_type)
    df.plot(x='ts', y=['lats'], kind='scatter', ax=ax, color='r', style='o', s=0.5, ylim=(0, 30000))
    ax.set_ylabel("Latency (us)")

def parse_job(file_name):
    df = pd.read_csv(file_name, usecols=columns)
    grouped = (df.groupby(['job']))
    
    for name, v in grouped:
        print(name)


'''
y_lab_str = 'cycle'
#y_lab_str = 'L1d miss ratio'
#main_str = "Latency, L1d miss ratio @ Core 14 vs. Time (sec)"
main_str = "Latency, CPU cycle @ Core 14 vs. Time (sec)"

parse_files = [
    #"../data/{0}/{0}_perf_L1-dcache-load-misses_perf.csv".format(time_str),
    #"../data/{0}/{0}_perf_L1-dcache-loads_perf.csv".format(time_str),
    "../data/{0}/{0}_perf_cycles_perf.csv".format(time_str),
]

fig, ax = plt.subplots()
ax2 = ax.twinx()


#plt.legend(legend_arr)
ax.set_xlabel(x_lab_str)
#plt.ylabel(y_lab_str)
plt.title(main_str)
plt.show()
'''
