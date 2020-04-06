#!/usr/bin/env bash
_DIR=/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-10-02_13-42-52_
for f in ${_DIR}/20*
    do
        echo ${f}
        sbatch ./template_.sh ${f}
        sleep 20

done
