# profile ycsb benchmark.
# author: Yingjun Wu <yingjun@comp.nus.edu.sg>
# date: March 5th, 2016

import os
import sys
import time

server1_name = "yingjunw@dev1.db.pdl.cmu.local"
server2_name = "yingjunw@dev2.db.pdl.cmu.local"

oltp_home = "~/oltpbench"

parameters = {
"$IP":  "localhost",
"$PORT": "57721",
"$SCALE_FACTOR": "1",
"$TIME":  "120",
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
start_peloton_valgrind_script = "valgrind --tool=callgrind --trace-children=yes peloton -D ./data > /dev/null 2>&1 &"
start_peloton_script = "peloton -D ./data > /dev/null 2>&1 &"
stop_peloton_script = "pg_ctl -D ./data stop"
start_ycsb_bench_script = "./oltpbenchmark -b ycsb -c " + cwd + "/" + config_filename + " --create=true --load=true --execute=true -s 5 -o outputfile"

def prepare_parameters(thread_num, read_ratio, insert_ratio, update_ratio):
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
        
def start_peloton_valgrind():
    os.system(stop_peloton_script)
    os.system(start_cleanup_script)
    os.system(start_peloton_valgrind_script)
    time.sleep(5)

def start_peloton():
    os.system(stop_peloton_script)
    os.system(start_cleanup_script)
    os.system(start_peloton_script)
    time.sleep(5)

def start_bench(thread_num, read_ratio, insert_ratio, update_ratio):
    # go to oltpbench directory
    os.chdir(os.path.expanduser(oltp_home))
    os.system(start_ycsb_bench_script + "_t" + str(thread_num) + "_" + str(read_ratio) + "_" + str(insert_ratio) + "_" + str(update_ratio))

def stop_peloton():
    # go back to cwd
    os.chdir(cwd)
    os.system(stop_peloton_script)

def collect_data(thread_num, read_ratio, insert_ratio, update_ratio):
    os.chdir(cwd)
    dir_name = "collected_data_t" + str(thread_num) + "_" + str(read_ratio) + "_" + str(insert_ratio) + "_" + str(update_ratio)
    os.system("rm -rf " + dir_name)
    os.system("mkdir " + dir_name)
    os.system("mv callgrind.out.* " + dir_name)

if __name__ == "__main__":
    if (len(sys.argv) != 6):
        print("usage: " + sys.argv[0] + " is_execute thread_num read_ratio insert_ratio update_ratio")
        exit(0)
    is_execute = int(sys.argv[1])
    thread_num = int(sys.argv[2])
    read_ratio = int(sys.argv[3])
    insert_ratio = int(sys.argv[4])
    update_ratio = int(sys.argv[5])
    
    total_ratio = read_ratio + insert_ratio + update_ratio
    if thread_num <= 0:
        print("thread num must be larger than 0!")
        exit(0)
    if total_ratio != 100:
        print("total ratio must be 100!")
        exit(0)

    print("thread_num = " + str(thread_num))
    print("read_ratio = " + str(read_ratio))
    print("insert_ratio = " + str(insert_ratio))
    print("update_ratio = " + str(update_ratio))

    if (is_execute != 0):
        prepare_parameters(thread_num, read_ratio, insert_ratio, update_ratio)
        start_peloton_valgrind()
        start_bench(thread_num, read_ratio, insert_ratio, update_ratio)
    else:
        stop_peloton()
        collect_data(thread_num, read_ratio, insert_ratio, update_ratio)
