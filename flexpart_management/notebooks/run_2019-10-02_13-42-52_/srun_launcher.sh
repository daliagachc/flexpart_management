#!/usr/bin/env bash

#conda activate b36backup
init_date="2018-05-12"
run_name='run_2019-10-02_13-42-52_'
base_path='/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/'
get_flx_python='/homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/notebooks/scripts/get_flx_log_pol_coords_taito_srun.py'
base_run_path="${base_path}${run_name}"
base_init_date="${base_run_path}${init_date}"
echo "${base_init_date}"

for day in ${base_run_path}/*-*-*; do
  if [[ "${day}" > "${base_init_date}" ]]; then
    for dom in d01 d02; do

      echo "${day}"
      echo ${dom}
      srun -t60 -p serial --mem 10000 -c 1 -n 1 \
        -e "${day}"/error_logpol%j.txt \
        -o "${day}"/output_logpol%j.txt \
        --chdir="${day}" \
        python3 -u ${get_flx_python} "${day}" ${dom} ${run_name} &
      sleep 10
    done
  fi
done
