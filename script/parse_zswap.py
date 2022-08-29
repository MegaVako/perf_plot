import csv
import re

ROW_PERIOD = 20

input_f = open("zswap_stat.out")
output_f = open("out_f.csv", "w+") # FIXME
writer = csv.writer(output_f)
first_row = []
data_row = []

for idx, row in enumerate(input_f.readlines()):
    curr_row = row.strip("\n")
    print(idx, curr_row) 

    row_split_eq = curr_row.split("=")
    row_split_space = re.split(r'\s{2,}', curr_row)

    mod = idx % ROW_PERIOD
    is_first_row = idx / ROW_PERIOD < 1

    if mod == 0:
        if idx > 0:
            writer.writerow(data_row)
        data_row = []

    if "STAT" in row_split_space[0]:
        continue


    if mod > 0 and mod < 5:
        data_row.append(int(row_split_eq[1]))
        if is_first_row:
            first_row.append(row_split_eq[0].strip(" "))

    if mod > 5 and mod < 16:
        data_row.append(int(row_split_eq[1]))
        if is_first_row:
            first_row.append(row_split_eq[0].strip(" "))

    if mod > 16:
        if is_first_row:
            if mod == 17:
                print(row_split_space)
                for tag in row_split_space[1:]:
                    first_row.append("mem_{0}".format(tag))

                for tag_idx, tag in enumerate(row_split_space[1:]):
                    if tag_idx == 3:
                        break;
                    first_row.append("swap_{0}".format(tag))
        if mod > 17:
            for num in row_split_space[1:]:
                data_row.append(int(num))

    if idx == ROW_PERIOD - 1:
        writer.writerow(first_row)
