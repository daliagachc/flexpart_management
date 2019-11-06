#!/usr/bin/env bash
for day in /homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-09-25_15-25-01_/*-*-*
    do
        for dom in d01 d02
            do
                sleep 1
                echo ${day}
                echo ${dom}
                srun -t60 -p serial --mem 10000 -c 1 -n 1 \
                -e ${day}/error_logpol%j.txt \
                -o ${day}/output_logpol%j.txt \
                --chdir=${day} \
                python3 -u\
                /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/notebooks/run_2019-09-25_15-25-01_/get_flx_log_pol_coords_taito_srun.py \
                ${day} ${dom}&
            done
    done

