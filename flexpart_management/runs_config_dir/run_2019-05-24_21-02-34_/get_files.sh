#rsync -avz aliagadi@taito-login3.csc.fi:/proj/atm/saltena/runs/run_2019_04_03_1/wrf2/namelist.input ./
#rsync -avz aliagadi@taito-login3.csc.fi:/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/flexwrf.input.forward1 ./
#rsync -avz aliagadi@taito-login3.csc.fi:/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/flexwrf.input.backward1 ./
#rsync -avz aliagadi@taito-login3.csc.fi:/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/flexwrf.input.backward2 ./
#rsync -azv --progress --compress-level=9 aliagadi@taito-login3.csc.fi:/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/for_chc_1 ./data_out/
#rsync -azv --progress --compress-level=9 aliagadi@taito-login3.csc.fi:/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/bac_chc_1 ./data_out/
#rsync -avz aliagadi@taito-login3.csc.fi:/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/flexwrf.input.backward1_chc ./
#rsync -avz aliagadi@taito-login3.csc.fi:/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/flexwrf.input.forward1_chc ./
#rsync -avz ./flexwrf.input.backward1_chc aliagadi@taito-login3.csc.fi:/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/
#rsync -avz ./flexwrf.input.forward1_chc aliagadi@taito-login3.csc.fi:/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/
#rsync -azv --progress --compress-level=9 ./f_in_for_chc_v02 aliagadi@taito-login3.csc.fi:/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/
from=aliagadi@taito-login3.csc.fi:'/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/run_*'
to='./'
to=aliagadi@taito-login3.csc.fi:'/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/'
from='./run_*'
from=aliagadi@taito-login3.csc.fi:'/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples/for_chc_1_mpi/'
to='./for_chc_1_mpi/'
echo $from
echo $to
rsync -azv --progress --compress-level=9  $from $to
