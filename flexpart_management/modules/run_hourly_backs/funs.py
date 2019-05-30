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
import flexpart_management.modules.mk_available.mk_Availabe as ma

# %%
def format_date(in_date):
    out_date=in_date.strftime('%Y%m%d %H%M%S')
    return out_date



def create_single_run(
        date_start_release: dt.datetime,
        release_time_h: int,
        hours_back_in_time: int,
        num_particles: int,
        path_wrf_files: str,
        path_simulation: str,
        input_template: str,
        run_temp_path: str,
        run_flex_name: str,
        run_dic: dict

):
    # %%
    # date_start_release = dt.datetime(2017,12,7,0,0)

    doms = [i for i in range(1, 5)]
    flx_input_name = 'flx.input.txt'
    path_flx_input = os.path.join(path_simulation, flx_input_name)
    # %%
    pref_dic = create_pref_dic(doms)
    path_avail_dic = create_path_avail_dic(doms, path_simulation)
    # %%
    os.makedirs(path_simulation, exist_ok=True)
    # %%
    date_end_simulation = date_end_release = date_start_release + dt.timedelta(hours=release_time_h)

    date_start_simulation = date_start_release - dt.timedelta(hours=hours_back_in_time)

    dic4template = create_template_dic(date_end_release, date_end_simulation,
                                       date_start_release, date_start_simulation,
                                       num_particles, path_avail_dic, path_simulation,
                                       path_wrf_files)
    create_flex_input_file(dic4template, input_template, path_flx_input)
    # %%
    create_avail_files(date_end_simulation, date_start_simulation,
                       path_avail_dic, path_wrf_files, pref_dic)

    run_flex_outpath = os.path.join(path_simulation,run_flex_name)

    run_dic1 = run_dic
    run_dic1['input_flex'] = path_flx_input
    create_run_flex_sh(run_temp_path,run_flex_outpath,run_dic)
    # %%
    # %%


def create_avail_files(date_end_simulation, date_start_simulation, path_avail_dic, path_wrf_files, pref_dic):
    for (k1, v1), (k2, v2) in zip(pref_dic.items(), path_avail_dic.items()):
        ma.create_avail_file(path_wrf_files, v2, v1, d1=date_start_simulation, d2=date_end_simulation)
        print(v1)


def create_flex_input_file(dic4template, input_template, path_flx_input):
    input_template_str = read_input_template_file(input_template)
    str_out = input_template_str.format(**dic4template)
    file = open(path_flx_input, 'w')
    file.write(str_out)
    file.close()


def read_input_template_file(input_template):
    # %%
    # Open a file: file
    file = open(input_template, mode='r')
    # read all lines at once
    input_template_str = file.read()
    # close the file
    file.close()
    return input_template_str


def create_template_dic(date_end_release, date_end_simulation, date_start_release, date_start_simulation, num_particles,
                        path_avail_dic, path_simulation, path_wrf_files):
    dic4template = dict(
        date_start_simulation_format=format_date(date_start_simulation),
        date_end_simulation_format=format_date(date_end_simulation),
        date_start_release_format=format_date(date_start_release),
        date_end_release_format=format_date(date_end_release),
        num_particles=num_particles,
        path_simulation=path_simulation,
        path_wrf_files=path_wrf_files,
        **path_avail_dic

    )
    return dic4template


def create_path_avail_dic(doms, path_simulation):
    path_avail_dic = {}
    for i in doms:
        val = os.path.join(path_simulation, 'avail0{}.txt'.format(i))
        key = 'path_avail_0{}'.format(i)
        path_avail_dic[key] = val
    return path_avail_dic


def create_pref_dic(doms):
    pref_dic = {}
    for i in doms:
        val = 'wrfout_d0{}'.format(i)
        key = 'prefix_0{}'.format(i)
        pref_dic[key] = val
    return pref_dic

def create_run_flex_sh(run_temp_path,run_flex_outpath,run_dic):
    run_str = read_input_template_file(run_temp_path)
    run_str_out = run_str.format(**run_dic)
    file = open(run_flex_outpath,'w')
    file.write(run_str_out)
    file.close()


