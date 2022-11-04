#!bin/bash -x

RAW_TIME=$(date '+%H_%M_%S')
RECORD_NAME="./raw_result/${RAW_TIME}"
mkdir -p results
mkdir $RAW_TIME
cd ../

# start perf
echo "perf on" >> "${RECORD_NAME}.txt"
date +"%T.%N" >> "${RECORD_NAME}.txt"

# monitor LLC
sudo perf record -e LLC-load-misses,LLC-store-misses,LLC-loads,LLC-stores,cycles&
PERF_PID=$!

# start running
# TODO, place your work here
# TODO, wait for your work to be done
sleep 10 # FIXME, dummy work

# done, kill monitoring processes
echo "perf kill" >> "${RECORD_NAME}.txt"
date +"%T.%N" >> "${RECORD_NAME}.txt"
sudo pkill -f perf

echo "wait for perf to complete"
sleep 20

sudo perf script > "${RECORD_NAME}_perf.txt"
python3 parse_perf.py "${RAW_TIME}_perf"

mv results/"${RAW_TIME}"* "results/${RAW_TIME}/"
# mv "results/${RAW_TIME}" "hpca_perf/data/"
