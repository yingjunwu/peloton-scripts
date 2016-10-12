# How to use?

This repository maintains the scripts for running Peloton with oltpbench (https://github.com/cmu-db/oltpbench). For now, we support YCSB and TPC-C benchmark. Before running the scripts, you must have already downloaded and compiled the oltpbench.

Following the steps below, you can run Peloton with oltpbench on a single machine.

1. Set the oltpbench directory: https://github.com/yingjunwu/peloton-scripts/blob/master/measure-performance.py#L9.

2. Copy measure-performance.py, tpcc_template.xml, and ycsb_template.xml to $PELOTON_HOME/build/.

3. Run ```python measure-performance.py``` to check the parameters to be passed.

You may use the following command to run YCSB benchmark containing 50% read and 50% write with 20 threads:
```
python measure-performance.py ycsb 0 20 10 50 0 50
```

You may use the following command to run TPC-C benchmark with 20 threads:
```
python measure-performance.py tpcc 0 20 20 45 43 4 4 4
```
