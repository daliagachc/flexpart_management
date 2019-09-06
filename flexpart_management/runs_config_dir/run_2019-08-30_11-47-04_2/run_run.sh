#!/usr/bin/env bash

for f in ./*/run_flex.sh
do
        echo ${f}
        dir=$(dirname ${f})
        cd $dir
        sbatch ./run_flex.sh
        mv ./run_flex.sh ./runned_flex.sh
        cd ..
done