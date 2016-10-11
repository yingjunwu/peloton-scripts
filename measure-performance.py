# profile ycsb benchmark.
# author: Yingjun Wu <yingjun@comp.nus.edu.sg>
# date: March 5th, 2016

import os
import sys
import time

oltp_home = "~/oltpbench"
peloton_port = "5432"

ycsb_parameters = {
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

tpcc_parameters = {
"$IP":  "localhost",
"$PORT": peloton_port,
"$SCALE_FACTOR": "1",
"$TIME":  "10",
"$THREAD_NUMBER": "1",
"$NEW_ORDER_RATIO": "0",
"$PAYMENT_RATIO": "0",
"$ORDER_STATUS_RATIO": "0",
"$DELIVERY_RATIO": "0",
"$STOCK_LEVEL_RATIO": "0"
}

cwd = os.getcwd()
ycsb_config_filename = "peloton_ycsb_config.xml"
tpcc_config_filename = "peloton_tpcc_config.xml"

start_cleanup_script = "rm -rf callgrind.out.*"

start_peloton_script = "./bin/peloton -port " + peloton_port + " > /dev/null 2>&1 &"
start_peloton_valgrind_script = "valgrind --tool=callgrind --trace-children=yes " + start_peloton_script

stop_peloton_script = "pkill -f peloton"

start_ycsb_bench_script = "./oltpbenchmark -b ycsb -c " + cwd + "/" + ycsb_config_filename + " --create=true --load=true --execute=true -s 5 -o outputfile | grep requests/sec >> peloton_ycsb_result"
start_tpcc_bench_script = "./oltpbenchmark -b tpcc -c " + cwd + "/" + tpcc_config_filename + " --create=true --load=true --execute=true -s 5 -o outputfile | grep requests/sec >> peloton_tpcc_result"


def prepare_ycsb_parameters(thread_num, read_ratio, insert_ratio, update_ratio):
    os.chdir(cwd)
    ycsb_parameters["$THREAD_NUMBER"] = str(thread_num)
    ycsb_parameters["$READ_RATIO"] = str(read_ratio)
    ycsb_parameters["$INSERT_RATIO"] = str(insert_ratio)
    ycsb_parameters["$UPDATE_RATIO"] = str(update_ratio)
    ycsb_template = ""
    with open("ycsb_template.xml") as in_file:
        ycsb_template = in_file.read()
    for param in ycsb_parameters:
        ycsb_template = ycsb_template.replace(param, ycsb_parameters[param])
    with open(ycsb_config_filename, "w") as out_file:
        out_file.write(ycsb_template)


def prepare_tpcc_parameters(thread_num, new_order_ratio, payment_ratio, order_status_ratio, delivery_ratio, stock_level_ratio):
    os.chdir(cwd)
    ycsb_parameters["$THREAD_NUMBER"] = str(thread_num)
    ycsb_parameters["$NEW_ORDER_RATIO"] = str(new_order_ratio)
    ycsb_parameters["$PAYMENT_RATIO"] = str(payment_ratio)
    ycsb_parameters["$ORDER_STATUS_RATIO"] = str(order_status_ratio)
    ycsb_parameters["$DELIVERY_RATIO"] = str(delivery_ratio)
    ycsb_parameters["$STOCK_LEVEL_RATIO"] = str(stock_level_ratio)
    ycsb_template = ""
    with open("tpcc_template.xml") as in_file:
        tpcc_template = in_file.read()
    for param in tpcc_parameters:
        tpcc_template = tpcc_template.replace(param, tpcc_parameters[param])
    with open(tpcc_config_filename, "w") as out_file:
        out_file.write(tpcc_template)


def start_peloton(is_profiling):
    os.chdir(cwd)
    os.system(stop_peloton_script)
    os.system(start_cleanup_script)
    if is_profiling:
        os.system(start_peloton_valgrind_script)
    else:
        os.system(start_peloton_script)
    time.sleep(2)

def start_ycsb_bench(thread_num, read_ratio, insert_ratio, update_ratio):
    # go to oltpbench directory
    os.chdir(os.path.expanduser(oltp_home))
    os.system(start_ycsb_bench_script + "_t" + str(thread_num) + "_" + str(read_ratio) + "_" + str(insert_ratio) + "_" + str(update_ratio))
    time.sleep(2)

def start_tpcc_bench(thread_num, new_order_ratio, payment_ratio, order_status_ratio, delivery_ratio, stock_level_ratio):
    # go to oltpbench directory
    os.chdir(os.path.expanduser(oltp_home))
    os.system(start_tpcc_bench_script + "_t" + str(thread_num) + "_" + str(new_order_ratio) + "_" + str(payment_ratio) + "_" + str(order_status_ratio) + "_" + str(delivery_ratio) + "_" + stock_level_ratio)
    time.sleep(2)


def stop_peloton():
    # go back to cwd
    os.chdir(cwd)
    os.system(stop_peloton_script)

if __name__ == "__main__":

    if (len(sys.argv) != 7 and len(sys.argv) != 9):
        print("usage: " + sys.argv[0] + "ycsb is_profiling thread_num read_ratio insert_ratio update_ratio")
        print("usage: " + sys.argv[0] + "tpcc is_profiling thread_num new_order_ratio payment_ratio order_status_ratio delivery_ratio stock_level_ratio")
        exit(0)

    if (len(sys.argv) == 7):
        is_profiling = int(sys.argv[2])
        thread_num = int(sys.argv[3])
        read_ratio = int(sys.argv[4])
        insert_ratio = int(sys.argv[5])
        update_ratio = int(sys.argv[6])
        
        print("thread_num = " + str(thread_num))
        print("read_ratio = " + str(read_ratio))
        print("insert_ratio = " + str(insert_ratio))
        print("update_ratio = " + str(update_ratio))

        prepare_ycsb_parameters(thread_num, read_ratio, insert_ratio, update_ratio)

        start_peloton(is_profiling)
        start_bench(thread_num, read_ratio, insert_ratio, update_ratio)
        stop_peloton()

    elif (len(sys.argv) == 9):
        is_profiling = int(sys.argv[2])
        thread_num = int(sys.argv[3])
        new_order_ratio = int(sys.argv[4])
        payment_ratio = int(sys.argv[5])
        order_status_ratio = int(sys.argv[6])
        delivery_ratio = int(sys.argv[7])
        stock_level_ratio = int(sys.argv[8])
        
        print("thread_num = " + str(thread_num))
        print("new_order_ratio = " + str(new_order_ratio))
        print("payment_ratio = " + str(payment_ratio))
        print("order_status_ratio = " + str(order_status_ratio))
        print("delivery_ratio = " + str(delivery_ratio))
        print("order_status_ratio = " + str(order_status_ratio))

        prepare_tpcc_parameters(thread_num, new_order_ratio, payment_ratio, order_status_ratio, delivery_ratio, stock_level_ratio)

        start_peloton(is_profiling)
        start_bench(thread_num, read_ratio, insert_ratio, update_ratio)
        stop_peloton()
