#!/usr/bin/env bash

# lets copy the files
local_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $local_dir
run_name=$(basename $local_dir)
echo "run_name=${run_name}" > ${local_dir}/run_name.sh
echo $local_dir
echo $run_name
taito_dir="/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/"${run_name}
echo $taito_dir
taito_log="aliagadi@taito-login3.csc.fi"
echo $taito_log

sed "s/\$run_name/${run_name}/g" ./flex_input_templ > ./flex_input

rsync -az --progress ${local_dir}/ $taito_log:$taito_dir


ssh $taito_log /bin/bash << EOF
    source ~/.source_module.sh
    cd $taito_dir
    sbatch ./run_flex.sh
EOF

