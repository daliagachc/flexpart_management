#!/usr/bin/env bash
_DIR=/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-10-02_13-42-52_/log_pol_3
for f in ${_DIR}/20*d01.nc
    do
        echo ${f}

        sbatch ./template_log.sh ${f}
        sleep 2

done
