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
from useful_scit.imps import *
import datetime as dt
from flexpart_management.modules.run_hourly_backs import funs





# %%
d1 = dt.datetime(2017,12,6)
d2 = dt.datetime(2017,12,26)

# %%
date_range = pd.date_range(d1,d2,freq='1H').values
source_run_path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/2019-05-30_01-38-03_'
path_wrf_files = '/proj/atm/saltena/runs/run_2019_05_15/wrf'

# %%

    

# %%
def create_run_from_d1(d1:dt.datetime,
                       source_run_path:str,
                       path_wrf_files:str,
                       ):
        # date_start_release = dt.datetime(2017, 12, 25, 3, 15)
        date_start_release = d1
        release_time_h = 1
        hours_back_in_time = 24
        num_particles = 10000
        # path_wrf_files = '/Users/diego/Downloads/wrf_test_d01/'  # 'where are the input files'
        input_template = './input_template.txt'
        run_name = date_start_release.strftime('%Y-%m-%d_%H_%M')
        path_simulation = os.path.join(source_run_path,run_name)  # 'where the simulation will be run'
        run_flex_name = 'run_flex.sh'
        run_temp_path = './run_flex_template.sh'
        run_flex_outpath = os.path.join(path_simulation, run_flex_name)
        run_dic = dict(
                flex_dir='/homeappl/home/aliagadi/appl_taito/FLEXPART-WRF_v3.3.2',
                flex_exe='flexwrf33_gnu_omp',
                # input_flex = 'run_name',
                cpu_num=1,
                run_time='04:00:00',
                run_type='serial',
                run_mem=4000,
                run_name='flex' + run_name
        )
        # %%
        funs.create_single_run(
                date_start_release,
                release_time_h,
                hours_back_in_time,
                num_particles,
                path_wrf_files,
                path_simulation,
                input_template,
                run_temp_path,
                run_flex_name,
                run_dic
        )


# %%
for d in date_range:
    dd=pd.Timestamp(d).to_pydatetime()  
    create_run_from_d1(dd,source_run_path,path_wrf_files)


# %%
