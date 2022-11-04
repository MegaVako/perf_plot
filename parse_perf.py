import csv
import sys

if len(sys.argv) < 2:
    print("usage: python3 pcm_to_cache.py <file_time>")
    quit()

input_name = sys.argv[1]
INPUT_FILE = './raw_result/{0}.txt'.format(input_name)
OUTPUT_FILE = './results/{0}_{1}_perf.csv'

input_f = open(INPUT_FILE, 'r')

data_arr_dict = {}

for idx, row in enumerate(input_f.readlines()):
    try:
        row_arr = row.strip().split()
        #print(row_arr)
        
        time = float(row_arr[-6][:-1])
        tag = row_arr[-4][:-1]
        process = row_arr[-9]
        count = int(row_arr[-5])
        cpu = int(row_arr[-7][1:-1])
        job = row_arr[-2]
        
        if tag not in data_arr_dict:
            data_arr_dict[tag] = []

        data_arr_dict[tag].append((time, count, process, cpu, job))
    except Exception as e:
        print(e)
        print(row.strip().split())

for k, v in data_arr_dict.items():
    out_f = open(OUTPUT_FILE.format(input_name, k), 'w+')
    writer = csv.writer(out_f)
    writer.writerow(["time", "count", 'process', 'cpu', 'job'])

    for time, cnt, process, cpu, job in v:
        writer.writerow([time, cnt, process, cpu, job])
