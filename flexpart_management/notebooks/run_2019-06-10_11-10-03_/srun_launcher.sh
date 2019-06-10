#!/usr/bin/env bash
for day in /homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-10_11-10-03_/*-*-*
    do
        for dom in d01 d02
            do
                echo ${day}
                echo ${dom}
                srun -t60 -p serial --mem 10000 -c 1\
                python3 -u\
                /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/notebooks/run_2019-06-10_11-10-03_/get_flx_log_pol_coords_taito_srun.py \
                ${day} ${dom}&
            done
    done
