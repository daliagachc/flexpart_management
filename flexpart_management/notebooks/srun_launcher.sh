#!/usr/bin/env bash
for day in /homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-05_18-42-11_/2017-12-11*
    do
        echo ${day}
        srun -t60 -p serial --mem 10000 -c 1\
        python3 -u\
        /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/notebooks/get_flx_log_pol_coords_taito_srun.py ${day} &
    done
