# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload
# %autoreload 2

# %%
import flexpart_management.modules.daily_back.config_file as cf
import flexpart_management.modules.daily_back.ConfigDayRun as cd
import pprint
import datetime as dt

# %%
run_base_name = 'run_2019-09-25_15-25-01_'

init_dic = dict(
    DATE_START=dt.date(2017, 12, 6),
    DATE_END=dt.date(2018, 5, 31),
    HOURS_BACK_IN_TIME=96,  # possitive,
    RUN_BASE_NAME=run_base_name,
    RUN_BASE_PATH='/Users/diego/flexpart_management/flexpart_management/runs_config_dir',
    RUN_BASE_PATH_TAITO='/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
    WRFOUT_PATH='/proj/atm/saltena/runs/run_2019_05_15/wrf',
    FLX_INPUT_TEMPL_PATH='/Users/diego/flexpart_management/flexpart_management/runs_config_dir/' \
                         + run_base_name + '/flex_input_templ',
    RUN_TEMPL_PATH='/Users/diego/flexpart_management/flexpart_management/runs_config_dir/' \
                   + run_base_name + '/run_flex_templ.sh',
    Z1_LEVEL=0.0,
    Z2_LEVEL=10.0,
    N_PARTICLES=20000,
    MASS_EMMITTED=1.0,
    RELEASE_NAME='chc',  # release base nameo,
    FLX_EXE='flexwrf33_gnu_serial',
    SBATCH_N=1,
    SBATCH_T='10:00:00',
    SBATCH_P='serial',
    SBATCH_M=8000,
    NUMBER_OF_RELEASES=24,
)

pprint.pprint(init_dic)

# %%
cmd = cd.ConfigMultiDayRun(init_dic=init_dic)

# %%
cmd.rsync_to_taito()