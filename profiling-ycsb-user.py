# profile ycsb benchmark.
# author: Yingjun Wu <yingjun@comp.nus.edu.sg>
# date: March 5th, 2016

import os


server1_name = "yingjunw@dev1.db.pdl.cmu.local"
server2_name = "yingjunw@dev2.db.pdl.cmu.local"

peloton_build_dir = "~/my-peloton/build"

if __name__ == "__main__":
    start_cleanup = "rm -rf callgrind.out.*"
    start_remote_script = "ssh " + server2_name + r' "source ~/.profile; cd ' + peloton_build_dir + r'; python profiling-ycsb-local.py"'
    collect_data = "scp " + server2_name + ":" + peloton_build_dir + "/callgrind.out.* ."

    os.system(start_cleanup)
    os.system(start_remote_script)
    os.system(collect_data)