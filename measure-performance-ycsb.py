# profile ycsb benchmark.
# author: Yingjun Wu <yingjun@comp.nus.edu.sg>
# date: March 5th, 2016

import os
import sys
import time

oltp_home = "~/oltpbench"
peloton_port = "5432"

parameters = {
"$IP":  "localhost",
"$PORT": peloton_port,
"$SCALE_FACTOR": "1",
"$TIME":  "10",
"$THREAD_NUMBER": "1",
"$READ_RATIO": "0",
"$INSERT_RATIO": "0",
"$SCAN_RATIO": "0",
"$UPDATE_RATIO": "0",
"$DELETE_RATIO": "0",
"$RMW_RATIO": "0"
}

cwd = os.getcwd()
config_filename = "peloton_ycsb_config.xml"

start_cleanup_script = "rm -rf callgrind.out.*"

start_peloton_script = "./bin/peloton -port " + peloton_port + " > /dev/null 2>&1 &"
start_peloton_valgrind_script = "valgrind --tool=callgrind --trace-children=yes " + start_peloton_script

stop_peloton_script = "pkill -9 peloton"

start_ycsb_bench_script = "./oltpbenchmark -b ycsb -c " + cwd + "/" + config_filename + " --create=true --load=true --execute=true -s 5 -o outputfile | grep requests/sec >> peloton_result"

def prepare_parameters(thread_num, read_ratio, insert_ratio, update_ratio):
    os.chdir(cwd)
    parameters["$THREAD_NUMBER"] = str(thread_num)
    parameters["$READ_RATIO"] = str(read_ratio)
    parameters["$INSERT_RATIO"] = str(insert_ratio)
    parameters["$UPDATE_RATIO"] = str(update_ratio)
    ycsb_template = ""
    with open("ycsb_template.xml") as in_file:
        ycsb_template = in_file.read()
    for param in parameters:
        ycsb_template = ycsb_template.replace(param, parameters[param])
    with open(config_filename, "w") as out_file:
        out_file.write(ycsb_template)

def start_peloton(is_profiling):
    os.chdir(cwd)
    os.system(stop_peloton_script)
    os.system(start_cleanup_script)
    if is_profiling:
        os.system(start_peloton_valgrind_script)
    else:
        os.system(start_peloton_script)
    time.sleep(2)

def start_bench(thread_num, read_ratio, insert_ratio, update_ratio):
    # go to oltpbench directory
    os.chdir(os.path.expanduser(oltp_home))
    os.system(start_ycsb_bench_script + "_t" + str(thread_num) + "_" + str(read_ratio) + "_" + str(insert_ratio) + "_" + str(update_ratio))
    time.sleep(2)

def stop_peloton():
    # go back to cwd
    os.chdir(cwd)
    os.system(stop_peloton_script)

if __name__ == "__main__":
    if (len(sys.argv) != 6):
        print("usage: " + sys.argv[0] + " is_profiling thread_num read_ratio insert_ratio update_ratio")
        exit(0)
    
    is_profiling = int(sys.argv[1])
    thread_num = int(sys.argv[2])
    read_ratio = int(sys.argv[3])
    insert_ratio = int(sys.argv[4])
    update_ratio = int(sys.argv[5])
    
    
    print("thread_num = " + str(thread_num))
    print("read_ratio = " + str(read_ratio))
    print("insert_ratio = " + str(insert_ratio))
    print("update_ratio = " + str(update_ratio))

    prepare_parameters(thread_num, read_ratio, insert_ratio, update_ratio)

    start_peloton(is_profiling)
    start_bench(thread_num, read_ratio, insert_ratio, update_ratio)
    stop_peloton()