# profile ycsb benchmark.
# author: Yingjun Wu <yingjun@comp.nus.edu.sg>
# date: March 5th, 2016

import os
import time

server1_name = "yingjunw@dev1.db.pdl.cmu.local"
server2_name = "yingjunw@dev2.db.pdl.cmu.local"

oltp_home = "~/oltpbench"

parameters = {
"$IP":  "localhost",
"$PORT": "57721",
"$SCALE_FACTOR": "100",
"$TIME":  "30",
"$THREAD_NUMBER": "1",
"$READ_RATIO": "50",
"$INSERT_RATIO": "50",
"$SCAN_RATIO": "0",
"$UPDATE_RATIO": "0",
"$DELETE_RATIO": "0",
"$RMW_RATIO": "0"
}

thread_num = 1
read_ratio = 0

def prepare_parameters():
    parameters["$THREAD_NUMBER"] = str(thread_num)
    parameters["$READ_RATIO"] = str(read_ratio)
    parameters["$INSERT_RATIO"] = str(100-read_ratio)
    ycsb_template = ""
    with open("peloton-scripts/ycsb_template.xml") as in_file:
        ycsb_template = in_file.read()
    for param in parameters:
        ycsb_template = ycsb_template.replace(param, parameters[param])
    with open("peloton_ycsb_config.xml", "w") as out_file:
        out_file.write(ycsb_template)
        
if __name__ == "__main__":
    prepare_parameters()
    cwd = os.getcwd()
    
    start_cleanup = "rm -rf callgrind.out.*"
    start_peloton_valgrind = "valgrind --tool=callgrind --trace-children=yes ./src/peloton -D ./data > /dev/null 2>&1 &"
    stop_peloton = "pg_ctl -D ./data stop"
    script_location = "peloton_ycsb_config.xml"
    start_ycsb_bench = "./oltpbenchmark -b ycsb -c " + script_location + " --create=true --load=false --execute=true -s 5 -o outputfile"
    
    os.system(stop_peloton)
    os.system(start_cleanup)
    os.system(start_peloton_valgrind)
    time.sleep(5)
    # go to oltpbench directory
    os.chdir(os.path.expanduser(oltp_home))
    os.system(start_ycsb_bench)
    # go back to cwd
    os.chdir(cwd)
    os.system(stop_peloton)

