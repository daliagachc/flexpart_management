```python
%load_ext autoreload
%autoreload 2
```

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload



```python
import flexpart_management.modules.daily_back.config_file as cf
import flexpart_management.modules.daily_back.ConfigDayRun as cd
import pprint
import datetime as dt
```


```python
init_dic = dict(
    DATE_START         =   dt.date(2017,12,6),
    DATE_END = dt.date(2018,1,17),
    HOURS_BACK_IN_TIME      =   96,   # possitive,
    RUN_BASE_NAME           =   'run_2019-06-03_23-35-40_',
    RUN_BASE_PATH           =   '/tmp/',
    RUN_BASE_PATH_TAITO     =   '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
    WRFOUT_PATH             =   '/proj/atm/saltena/runs/run_2019_05_15/wrf',
    FLX_INPUT_TEMPL_PATH    =   '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
    RUN_TEMPL_PATH          =   '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
    Z1_LEVEL                =   0.0,
    Z2_LEVEL                =   10.0,
    N_PARTICLES             =   1000000,
    MASS_EMMITTED           =   1.0,
    RELEASE_NAME            =   'chc', # release base nameo,
    FLX_EXE                 =   'flexwrf33_gnu_omp',
    SBATCH_N                = 4,
    SBATCH_T                = '05:00:00',
    SBATCH_P                = 'parallel',
    SBATCH_M                = 8000,
)
```


```python
cmd = cd.ConfigMultiDayRun(init_dic)
```


```python
cmd.__dict__
```




    {'INIT_DIC': {'HOURS_BACK_IN_TIME': 96,
      'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
      'RUN_BASE_PATH': '/tmp/',
      'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
      'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
      'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
      'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
      'Z1_LEVEL': 0.0,
      'Z2_LEVEL': 10.0,
      'N_PARTICLES': 100000,
      'MASS_EMMITTED': 1.0,
      'RELEASE_NAME': 'chc',
      'FLX_EXE': 'flexwrf33_gnu_omp',
      'SBATCH_N': 2,
      'SBATCH_T': '02:00:00',
      'SBATCH_P': 'parallel',
      'SBATCH_M': 8000},
     'DATE_START': datetime.date(2017, 12, 10),
     'DATE_END': datetime.date(2017, 12, 20),
     'DATE_RANGE': array([datetime.datetime(2017, 12, 10, 0, 0),
            datetime.datetime(2017, 12, 11, 0, 0),
            datetime.datetime(2017, 12, 12, 0, 0),
            datetime.datetime(2017, 12, 13, 0, 0),
            datetime.datetime(2017, 12, 14, 0, 0),
            datetime.datetime(2017, 12, 15, 0, 0),
            datetime.datetime(2017, 12, 16, 0, 0),
            datetime.datetime(2017, 12, 17, 0, 0),
            datetime.datetime(2017, 12, 18, 0, 0),
            datetime.datetime(2017, 12, 19, 0, 0),
            datetime.datetime(2017, 12, 20, 0, 0)], dtype=object),
     'DICS_FOR_DAY_RUN': [{'HOURS_BACK_IN_TIME': 96,
       'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
       'RUN_BASE_PATH': '/tmp/',
       'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
       'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
       'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
       'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
       'Z1_LEVEL': 0.0,
       'Z2_LEVEL': 10.0,
       'N_PARTICLES': 100000,
       'MASS_EMMITTED': 1.0,
       'RELEASE_NAME': 'chc',
       'FLX_EXE': 'flexwrf33_gnu_omp',
       'SBATCH_N': 2,
       'SBATCH_T': '02:00:00',
       'SBATCH_P': 'parallel',
       'SBATCH_M': 8000,
       'DATE_SIMULATION': datetime.datetime(2017, 12, 10, 0, 0)},
      {'HOURS_BACK_IN_TIME': 96,
       'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
       'RUN_BASE_PATH': '/tmp/',
       'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
       'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
       'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
       'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
       'Z1_LEVEL': 0.0,
       'Z2_LEVEL': 10.0,
       'N_PARTICLES': 100000,
       'MASS_EMMITTED': 1.0,
       'RELEASE_NAME': 'chc',
       'FLX_EXE': 'flexwrf33_gnu_omp',
       'SBATCH_N': 2,
       'SBATCH_T': '02:00:00',
       'SBATCH_P': 'parallel',
       'SBATCH_M': 8000,
       'DATE_SIMULATION': datetime.datetime(2017, 12, 11, 0, 0)},
      {'HOURS_BACK_IN_TIME': 96,
       'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
       'RUN_BASE_PATH': '/tmp/',
       'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
       'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
       'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
       'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
       'Z1_LEVEL': 0.0,
       'Z2_LEVEL': 10.0,
       'N_PARTICLES': 100000,
       'MASS_EMMITTED': 1.0,
       'RELEASE_NAME': 'chc',
       'FLX_EXE': 'flexwrf33_gnu_omp',
       'SBATCH_N': 2,
       'SBATCH_T': '02:00:00',
       'SBATCH_P': 'parallel',
       'SBATCH_M': 8000,
       'DATE_SIMULATION': datetime.datetime(2017, 12, 12, 0, 0)},
      {'HOURS_BACK_IN_TIME': 96,
       'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
       'RUN_BASE_PATH': '/tmp/',
       'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
       'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
       'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
       'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
       'Z1_LEVEL': 0.0,
       'Z2_LEVEL': 10.0,
       'N_PARTICLES': 100000,
       'MASS_EMMITTED': 1.0,
       'RELEASE_NAME': 'chc',
       'FLX_EXE': 'flexwrf33_gnu_omp',
       'SBATCH_N': 2,
       'SBATCH_T': '02:00:00',
       'SBATCH_P': 'parallel',
       'SBATCH_M': 8000,
       'DATE_SIMULATION': datetime.datetime(2017, 12, 13, 0, 0)},
      {'HOURS_BACK_IN_TIME': 96,
       'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
       'RUN_BASE_PATH': '/tmp/',
       'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
       'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
       'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
       'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
       'Z1_LEVEL': 0.0,
       'Z2_LEVEL': 10.0,
       'N_PARTICLES': 100000,
       'MASS_EMMITTED': 1.0,
       'RELEASE_NAME': 'chc',
       'FLX_EXE': 'flexwrf33_gnu_omp',
       'SBATCH_N': 2,
       'SBATCH_T': '02:00:00',
       'SBATCH_P': 'parallel',
       'SBATCH_M': 8000,
       'DATE_SIMULATION': datetime.datetime(2017, 12, 14, 0, 0)},
      {'HOURS_BACK_IN_TIME': 96,
       'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
       'RUN_BASE_PATH': '/tmp/',
       'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
       'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
       'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
       'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
       'Z1_LEVEL': 0.0,
       'Z2_LEVEL': 10.0,
       'N_PARTICLES': 100000,
       'MASS_EMMITTED': 1.0,
       'RELEASE_NAME': 'chc',
       'FLX_EXE': 'flexwrf33_gnu_omp',
       'SBATCH_N': 2,
       'SBATCH_T': '02:00:00',
       'SBATCH_P': 'parallel',
       'SBATCH_M': 8000,
       'DATE_SIMULATION': datetime.datetime(2017, 12, 15, 0, 0)},
      {'HOURS_BACK_IN_TIME': 96,
       'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
       'RUN_BASE_PATH': '/tmp/',
       'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
       'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
       'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
       'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
       'Z1_LEVEL': 0.0,
       'Z2_LEVEL': 10.0,
       'N_PARTICLES': 100000,
       'MASS_EMMITTED': 1.0,
       'RELEASE_NAME': 'chc',
       'FLX_EXE': 'flexwrf33_gnu_omp',
       'SBATCH_N': 2,
       'SBATCH_T': '02:00:00',
       'SBATCH_P': 'parallel',
       'SBATCH_M': 8000,
       'DATE_SIMULATION': datetime.datetime(2017, 12, 16, 0, 0)},
      {'HOURS_BACK_IN_TIME': 96,
       'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
       'RUN_BASE_PATH': '/tmp/',
       'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
       'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
       'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
       'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
       'Z1_LEVEL': 0.0,
       'Z2_LEVEL': 10.0,
       'N_PARTICLES': 100000,
       'MASS_EMMITTED': 1.0,
       'RELEASE_NAME': 'chc',
       'FLX_EXE': 'flexwrf33_gnu_omp',
       'SBATCH_N': 2,
       'SBATCH_T': '02:00:00',
       'SBATCH_P': 'parallel',
       'SBATCH_M': 8000,
       'DATE_SIMULATION': datetime.datetime(2017, 12, 17, 0, 0)},
      {'HOURS_BACK_IN_TIME': 96,
       'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
       'RUN_BASE_PATH': '/tmp/',
       'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
       'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
       'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
       'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
       'Z1_LEVEL': 0.0,
       'Z2_LEVEL': 10.0,
       'N_PARTICLES': 100000,
       'MASS_EMMITTED': 1.0,
       'RELEASE_NAME': 'chc',
       'FLX_EXE': 'flexwrf33_gnu_omp',
       'SBATCH_N': 2,
       'SBATCH_T': '02:00:00',
       'SBATCH_P': 'parallel',
       'SBATCH_M': 8000,
       'DATE_SIMULATION': datetime.datetime(2017, 12, 18, 0, 0)},
      {'HOURS_BACK_IN_TIME': 96,
       'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
       'RUN_BASE_PATH': '/tmp/',
       'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
       'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
       'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
       'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
       'Z1_LEVEL': 0.0,
       'Z2_LEVEL': 10.0,
       'N_PARTICLES': 100000,
       'MASS_EMMITTED': 1.0,
       'RELEASE_NAME': 'chc',
       'FLX_EXE': 'flexwrf33_gnu_omp',
       'SBATCH_N': 2,
       'SBATCH_T': '02:00:00',
       'SBATCH_P': 'parallel',
       'SBATCH_M': 8000,
       'DATE_SIMULATION': datetime.datetime(2017, 12, 19, 0, 0)},
      {'HOURS_BACK_IN_TIME': 96,
       'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
       'RUN_BASE_PATH': '/tmp/',
       'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
       'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
       'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
       'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
       'Z1_LEVEL': 0.0,
       'Z2_LEVEL': 10.0,
       'N_PARTICLES': 100000,
       'MASS_EMMITTED': 1.0,
       'RELEASE_NAME': 'chc',
       'FLX_EXE': 'flexwrf33_gnu_omp',
       'SBATCH_N': 2,
       'SBATCH_T': '02:00:00',
       'SBATCH_P': 'parallel',
       'SBATCH_M': 8000,
       'DATE_SIMULATION': datetime.datetime(2017, 12, 20, 0, 0)}]}




```python
init_dic.pop('sdf',None)
init_dic.pop('DATE_START',None)
```




    datetime.date(2017, 12, 10)




```python
init_dic
```




    {'DATE_END': datetime.date(2017, 12, 20),
     'HOURS_BACK_IN_TIME': 96,
     'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
     'RUN_BASE_PATH': '/tmp/',
     'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
     'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
     'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
     'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
     'Z1_LEVEL': 0.0,
     'Z2_LEVEL': 10.0,
     'N_PARTICLES': 100000,
     'MASS_EMMITTED': 1.0,
     'RELEASE_NAME': 'chc',
     'FLX_EXE': 'flexwrf33_gnu_omp',
     'SBATCH_N': 2,
     'SBATCH_T': '02:00:00',
     'SBATCH_P': 'parallel',
     'SBATCH_M': 8000}




```python
dr = cd.ConfigDayRun(init_dic=init_dic)
```


```python
from typing import TypedDict
```


    ---------------------------------------------------------------------------

    ImportError                               Traceback (most recent call last)

    <ipython-input-54-3e5877349209> in <module>
    ----> 1 from typing import TypedDict
    

    ImportError: cannot import name 'TypedDict'



```python
dr=cf.DayRun(init_dic=dict(A=12))
```


```python
dic = dr.get_class_dict()
pprint.pprint(dic)
```

    {'A': 12,
     'AVAILABLE_FILE_BASE_NAME': 'AVAILABLE',
     'AVAILABLE_PATHS': ['/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10/AVAILABLE01',
                         '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10/AVAILABLE02',
                         '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10/AVAILABLE03',
                         '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10/AVAILABLE04'],
     'DATE_SIMULATION': datetime.date(2017, 12, 10),
     'DAY_PATH': '/tmp/run_2019-06-02_20-42-05_/2017-12-10',
     'DAY_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10',
     'DOMAINS': ['01', '02', '03', '04'],
     'DT_END_SIMULATION': datetime.datetime(2017, 12, 11, 0, 0),
     'DT_FIRST_RELEASE': datetime.datetime(2017, 12, 10, 0, 0),
     'DT_LAST_RELEASE': datetime.datetime(2017, 12, 10, 23, 0),
     'DT_START_SIMULATION': datetime.datetime(2017, 12, 6, 0, 0),
     'FLX_EXE': 'flexwrf33_gnu_omp',
     'FLX_INPUT_BASE_NAME': 'flx_input',
     'FLX_INPUT_PATH': '/tmp/run_2019-06-02_20-42-05_/2017-12-10/flx_input',
     'FLX_INPUT_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10/flx_input',
     'FLX_INPUT_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ',
     'FRQ_SIMULATION_M': 15,
     'FRQ_WRFOUT_FILES_M': 60,
     'HOURS_BACK_IN_TIME': 96,
     'INPUT_TEMPL_STR': '=====================FORMER PATHNAMES '
                        'FILE===================\n'
                        '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10/\n'
                        '/proj/atm/saltena/runs/run_2019_05_15/wrf/\n'
                        '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10/AVAILABLE01\n'
                        '/proj/atm/saltena/runs/run_2019_05_15/wrf/\n'
                        '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10/AVAILABLE02\n'
                        '/proj/atm/saltena/runs/run_2019_05_15/wrf/\n'
                        '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10/AVAILABLE03\n'
                        '/proj/atm/saltena/runs/run_2019_05_15/wrf/\n'
                        '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10/AVAILABLE04\n'
                        '=============================================================\n'
                        '=====================FORMER COMMAND '
                        'FILE=====================\n'
                        '    -1               LDIRECT:          1 for forward '
                        'simulation, -1 for backward simulation\n'
                        '    20171206 000000  YYYYMMDD HHMISS   beginning date of '
                        'simulation\n'
                        '    20171211 000000  YYYYMMDD HHMISS   ending date of '
                        'simulation\n'
                        '    3600             SSSSS  (int)      output every SSSSS '
                        'seconds\n'
                        '    3600             SSSSS  (int)      time average of '
                        'output (in SSSSS seconds)\n'
                        '    180              SSSSS  (int)      sampling rate of '
                        'output (in SSSSS seconds)\n'
                        '    43200        SSSSS  (int)      time constant for '
                        'particle splitting (in seconds)\n'
                        '    180              SSSSS  (int)      synchronisation '
                        'interval of flexpart (in seconds)\n'
                        '    10.              CTL    (real)     factor by which '
                        'time step must be smaller than tl\n'
                        '    10               IFINE  (int)      decrease of time '
                        'step for vertical motion by factor ifine\n'
                        '    5                IOUT              1 concentration, 2 '
                        'mixing ratio, 3 both, 4 plume traject, 5=1+4\n'
                        '    1                IPOUT             particle dump: 0 '
                        'no, 1 every output interval, 2 only at end\n'
                        '    1                LSUBGRID          subgrid terrain '
                        'effect parameterization: 1 yes, 0 no\n'
                        '    0                LCONVECTION       convection: 3 yes, '
                        '0 no\n'
                        '    3600.            DT_CONV  (real)   time interval to '
                        'call convection, seconds\n'
                        '    1                LAGESPECTRA       age spectra: 1 '
                        'yes, 0 no\n'
                        '    0                IPIN              continue '
                        'simulation with dumped particle data: 1 yes, 0 no\n'
                        '    1                IFLUX             calculate fluxes: '
                        '1 yes, 0 no\n'
                        '    1                IOUTPUTFOREACHREL CREATE AN OUPUT '
                        'FILE FOR EACH RELEASE LOCATION: 1 YES, 0 NO\n'
                        '    0                MDOMAINFILL       domain-filling '
                        'trajectory option: 1 yes, 0 no, 2 strat. o3 tracer\n'
                        '    2                IND_SOURCE        1=mass unit , '
                        '2=mass mixing ratio unit\n'
                        '    2                IND_RECEPTOR      1=mass unit , '
                        '2=mass mixing ratio unit\n'
                        '    1                NESTED_OUTPUT     shall nested '
                        'output be used? 1 yes, 0 no\n'
                        '    0                LINIT_COND   INITIAL COND. FOR BW '
                        'RUNS: 0=NO,1=MASS UNIT,2=MASS MIXING RATIO UNIT\n'
                        '    1                TURB_OPTION       0=no turbulence; '
                        '1=diagnosed as in flexpart_ecmwf; 2 and 3=from tke.\n'
                        '    1                LU_OPTION         0=old landuse '
                        '(IGBP.dat); 1=landuse from WRF\n'
                        '    0                CBL SCHEME        0=no, 1=yes. works '
                        'if TURB_OPTION=1\n'
                        '    1                SFC_OPTION        0=default '
                        'computation of u*, hflux, pblh, 1=from wrf\n'
                        '    0                WIND_OPTION       0=snapshot winds, '
                        '1=mean winds,2=snapshot eta-dot,-1=w based on divergence\n'
                        '    0                TIME_OPTION       1=correction of '
                        'time validity for time-average wind,  0=no need\n'
                        '    0                OUTGRID_COORD     0=wrf '
                        'grid(meters), 1=regular lat/lon grid\n'
                        '    1                RELEASE_COORD     0=wrf '
                        'grid(meters), 1=regular lat/lon grid\n'
                        '    2                IOUTTYPE          0=default binary, '
                        '1=ascii (for particle dump only),2=netcdf\n'
                        '    1               NCTIMEREC (int)   Time frames per '
                        'output file, only used for netcdf\n'
                        '    100                VERBOSE           VERBOSE '
                        'MODE,0=minimum, 100=maximum\n'
                        '=====================FORMER AGECLASESS '
                        'FILE==================\n'
                        '    1                NAGECLASS        number of age '
                        'classes\n'
                        '    345600           SSSSSS  (int)    age class in SSSSS '
                        'seconds\n'
                        '=====================FORMER OUTGRID '
                        'FILE=====================\n'
                        '    0.0000000        OUTLONLEFT      geograhical '
                        'longitude of lower left corner of output grid\n'
                        '    0.0000000         OUTLATLOWER     geographical '
                        'latitude of lower left corner of output grid\n'
                        '    468               NUMXGRID        number of grid '
                        'points in x direction (= # of cells )\n'
                        '    340               NUMYGRID        number of grid '
                        'points in y direction (= # of cells )\n'
                        '    0                OUTGRIDDEF      outgrid defined '
                        '0=using grid distance, 1=upperright corner coordinate\n'
                        '    9500.0           DXOUTLON        grid distance in x '
                        'direction or upper right corner of output grid\n'
                        '    9500.0           DYOUTLON        grid distance in y '
                        'direction or upper right corner of output grid\n'
                        '    22               NUMZGRID        number of vertical '
                        'levels\n'
                        '    50               LEVEL           height of level '
                        '(upper boundary)\n'
                        '    100              LEVEL           height of level '
                        '(upper boundary)\n'
                        '    200              LEVEL           height of level '
                        '(upper boundary)\n'
                        '    300              LEVEL           height of level '
                        '(upper boundary)\n'
                        '    400              LEVEL           height of level '
                        '(upper boundary)\n'
                        '    500              LEVEL           height of level '
                        '(upper boundary)\n'
                        '    1000             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    1500             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    2000             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    2500             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    3000             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    3500             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    4000             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    4500             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    5000             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    6000             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    7000             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    8000             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    9000             LEVEL           height of level '
                        '(upper boundary)\n'
                        '    10000            LEVEL           height of level '
                        '(upper boundary)\n'
                        '    20000            LEVEL           height of level '
                        '(upper boundary)\n'
                        '    30000            LEVEL           height of level '
                        '(upper boundary)\n'
                        '================OUTGRID_NEST==========================\n'
                        '    1966500.0            OUTLONLEFT      geograhical '
                        'longitude of lower left corner of output grid\n'
                        '    1608670.0              OUTLATLOWER     geographical '
                        'latitude of lower left corner of output grid\n'
                        '    153               NUMXGRID        number of grid '
                        'points in x direction (= # of cells )\n'
                        '    150               NUMYGRID        number of grid '
                        'points in y direction (= # of cells )\n'
                        '    0                OUTGRIDDEF      outgrid defined '
                        '0=using grid distance, 1=upperright corner coordinate\n'
                        '    1055.5556           DXOUTLON        grid distance in '
                        'x direction or upper right corner of output grid\n'
                        '    1055.5556           DYOUTLON        grid distance in '
                        'y direction or upper right corner of output grid\n'
                        '=====================FORMER RECEPTOR '
                        'FILE====================\n'
                        '    0                NUMRECEPTOR     number of receptors\n'
                        '=====================FORMER SPECIES '
                        'FILE=====================\n'
                        '     1               NUMTABLE        number of variable '
                        'properties. The following lines are fixed format\n'
                        'XXXX|NAME    |decaytime |wetscava  '
                        '|wetsb|drydif|dryhenry|drya|partrho  '
                        '|parmean|partsig|dryvelo|weight |\n'
                        '    AIRTRACER     -999.9   -9.9E-09         '
                        '-9.9                 -9.9E09                   -9.99   '
                        '29.00\n'
                        '=====================FORMER RELEEASES '
                        'FILE===================\n'
                        '    1                   NSPEC           total number of '
                        'species emitted\n'
                        '    0                   EMITVAR         1 for emission '
                        'variation\n'
                        '    1                   LINK            index of species '
                        'in file SPECIES\n'
                        '    24                   NUMPOINT        number of '
                        'releases\n'
                        '  20171210 000000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 010000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_00    NAME OF RELEASE LOCATION\n'
                        '  20171210 010000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 020000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_01    NAME OF RELEASE LOCATION\n'
                        '  20171210 020000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 030000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_02    NAME OF RELEASE LOCATION\n'
                        '  20171210 030000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 040000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_03    NAME OF RELEASE LOCATION\n'
                        '  20171210 040000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 050000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_04    NAME OF RELEASE LOCATION\n'
                        '  20171210 050000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 060000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_05    NAME OF RELEASE LOCATION\n'
                        '  20171210 060000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 070000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_06    NAME OF RELEASE LOCATION\n'
                        '  20171210 070000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 080000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_07    NAME OF RELEASE LOCATION\n'
                        '  20171210 080000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 090000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_08    NAME OF RELEASE LOCATION\n'
                        '  20171210 090000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 100000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_09    NAME OF RELEASE LOCATION\n'
                        '  20171210 100000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 110000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_10    NAME OF RELEASE LOCATION\n'
                        '  20171210 110000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 120000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_11    NAME OF RELEASE LOCATION\n'
                        '  20171210 120000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 130000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_12    NAME OF RELEASE LOCATION\n'
                        '  20171210 130000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 140000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_13    NAME OF RELEASE LOCATION\n'
                        '  20171210 140000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 150000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_14    NAME OF RELEASE LOCATION\n'
                        '  20171210 150000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 160000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_15    NAME OF RELEASE LOCATION\n'
                        '  20171210 160000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 170000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_16    NAME OF RELEASE LOCATION\n'
                        '  20171210 170000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 180000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_17    NAME OF RELEASE LOCATION\n'
                        '  20171210 180000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 190000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_18    NAME OF RELEASE LOCATION\n'
                        '  20171210 190000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 200000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_19    NAME OF RELEASE LOCATION\n'
                        '  20171210 200000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 210000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_20    NAME OF RELEASE LOCATION\n'
                        '  20171210 210000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 220000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_21    NAME OF RELEASE LOCATION\n'
                        '  20171210 220000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171210 230000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_22    NAME OF RELEASE LOCATION\n'
                        '  20171210 230000       ID1, IT1        beginning date '
                        'and time of release\n'
                        '  20171211 000000       ID2, IT2        ending date and '
                        'time of release\n'
                        '  -68.140000            XPOINT1 (real)  longitude [deg] '
                        'of lower left corner\n'
                        '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                        'lower left corner\n'
                        '  -68.118000            XPOINT2 (real)  longitude [deg] '
                        'of upper right corner\n'
                        '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                        'upper right corner\n'
                        '  1                     KINDZ  (int)  1 for m above '
                        'ground, 2 for m above sea level, 3 pressure\n'
                        '  0.0                 ZPOINT1 (real)  lower z-level\n'
                        '  10.0                ZPOINT2 (real)  upper z-level\n'
                        '  100000                 NPART (int)     total number of '
                        'particles to be released\n'
                        '  1.0                XMASS (real)    total mass emitted\n'
                        '  chc20171210_23    NAME OF RELEASE LOCATION\n'
                        '\n',
     'MASS_EMMITTED': 1.0,
     'NUMBER_OF_RELEASES': 24,
     'N_PARTICLES': 100000,
     'RELEASE_FRQ': 1,
     'RELEASE_NAME': 'chc',
     'RELEASE_STR': '  20171210 000000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 010000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_00    NAME OF RELEASE LOCATION\n'
                    '  20171210 010000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 020000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_01    NAME OF RELEASE LOCATION\n'
                    '  20171210 020000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 030000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_02    NAME OF RELEASE LOCATION\n'
                    '  20171210 030000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 040000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_03    NAME OF RELEASE LOCATION\n'
                    '  20171210 040000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 050000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_04    NAME OF RELEASE LOCATION\n'
                    '  20171210 050000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 060000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_05    NAME OF RELEASE LOCATION\n'
                    '  20171210 060000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 070000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_06    NAME OF RELEASE LOCATION\n'
                    '  20171210 070000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 080000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_07    NAME OF RELEASE LOCATION\n'
                    '  20171210 080000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 090000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_08    NAME OF RELEASE LOCATION\n'
                    '  20171210 090000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 100000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_09    NAME OF RELEASE LOCATION\n'
                    '  20171210 100000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 110000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_10    NAME OF RELEASE LOCATION\n'
                    '  20171210 110000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 120000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_11    NAME OF RELEASE LOCATION\n'
                    '  20171210 120000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 130000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_12    NAME OF RELEASE LOCATION\n'
                    '  20171210 130000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 140000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_13    NAME OF RELEASE LOCATION\n'
                    '  20171210 140000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 150000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_14    NAME OF RELEASE LOCATION\n'
                    '  20171210 150000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 160000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_15    NAME OF RELEASE LOCATION\n'
                    '  20171210 160000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 170000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_16    NAME OF RELEASE LOCATION\n'
                    '  20171210 170000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 180000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_17    NAME OF RELEASE LOCATION\n'
                    '  20171210 180000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 190000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_18    NAME OF RELEASE LOCATION\n'
                    '  20171210 190000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 200000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_19    NAME OF RELEASE LOCATION\n'
                    '  20171210 200000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 210000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_20    NAME OF RELEASE LOCATION\n'
                    '  20171210 210000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 220000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_21    NAME OF RELEASE LOCATION\n'
                    '  20171210 220000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171210 230000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_22    NAME OF RELEASE LOCATION\n'
                    '  20171210 230000       ID1, IT1        beginning date and '
                    'time of release\n'
                    '  20171211 000000       ID2, IT2        ending date and time '
                    'of release\n'
                    '  -68.140000            XPOINT1 (real)  longitude [deg] of '
                    'lower left corner\n'
                    '  -16.355000            YPOINT1 (real)  latitude [deg] of '
                    'lower left corner\n'
                    '  -68.118000            XPOINT2 (real)  longitude [deg] of '
                    'upper right corner\n'
                    '  -16.335000            YPOINT2 (real)  latitude [DEG] of '
                    'upper right corner\n'
                    '  1                     KINDZ  (int)  1 for m above ground, 2 '
                    'for m above sea level, 3 pressure\n'
                    '  0.0                 ZPOINT1 (real)  lower z-level\n'
                    '  10.0                ZPOINT2 (real)  upper z-level\n'
                    '  100000                 NPART (int)     total number of '
                    'particles to be released\n'
                    '  1.0                XMASS (real)    total mass emitted\n'
                    '  chc20171210_23    NAME OF RELEASE LOCATION',
     'RUN_BASE_NAME': 'run_2019-06-02_20-42-05_',
     'RUN_BASE_PATH': '/tmp/',
     'RUN_BASE_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/',
     'RUN_FLX_BASE_NAME': 'run_flex.sh',
     'RUN_FLX_PATH': '/tmp/run_2019-06-02_20-42-05_/2017-12-10/run_flex.sh',
     'RUN_FLX_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10/run_flex.sh',
     'RUN_FLX_PATH_TEST': '/tmp/run_2019-06-02_20-42-05_/2017-12-10/run_flex_test.sh',
     'RUN_FLX_PATH_TEST_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_/2017-12-10/run_flex_test.sh',
     'RUN_FLX_TEST_BASE_NAME': 'run_flex_test.sh',
     'RUN_PATH': '/tmp/run_2019-06-02_20-42-05_',
     'RUN_PATH_TAITO': '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-02_20-42-05_',
     'RUN_TEMPL_PATH': '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh',
     'SBATCH_M': 8000,
     'SBATCH_N': 2,
     'SBATCH_P': 'parallel',
     'SBATCH_T': '02:00:00',
     'WRFOUT_PATH': '/proj/atm/saltena/runs/run_2019_05_15/wrf',
     'Z1_LEVEL': 0.0,
     'Z2_LEVEL': 10.0}



```python
dr.FLX_EXE
```




    'flexwrf33_gnu_omp'




```python

```


```python
variables
```




    ['AVAILABLE_FILE_BASE_NAME',
     'AVAILABLE_PATHS',
     'DATE_SIMULATION',
     'DAY_PATH',
     'DAY_PATH_TAITO',
     'DOMAINS',
     'DT_END_SIMULATION',
     'DT_FIRST_RELEASE',
     'DT_LAST_RELEASE',
     'DT_START_SIMULATION',
     'FLX_EXE',
     'FLX_INPUT_BASE_NAME',
     'FLX_INPUT_PATH',
     'FLX_INPUT_PATH_TAITO',
     'FLX_INPUT_TEMPL_PATH',
     'FRQ_SIMULATION_M',
     'FRQ_WRFOUT_FILES_M',
     'HOURS_BACK_IN_TIME',
     'INPUT_TEMPL_STR',
     'MASS_EMMITTED',
     'NUMBER_OF_RELEASES',
     'N_PARTICLES',
     'RELEASE_FRQ',
     'RELEASE_NAME',
     'RELEASE_STR',
     'RUN_BASE_NAME',
     'RUN_BASE_PATH',
     'RUN_BASE_PATH_TAITO',
     'RUN_FLX_BASE_NAME',
     'RUN_FLX_PATH',
     'RUN_FLX_PATH_TAITO',
     'RUN_FLX_PATH_TEST',
     'RUN_FLX_PATH_TEST_TAITO',
     'RUN_FLX_TEST_BASE_NAME',
     'RUN_PATH',
     'RUN_PATH_TAITO',
     'RUN_TEMPL_PATH',
     'SBATCH_M',
     'SBATCH_N',
     'SBATCH_P',
     'SBATCH_T',
     'WRFOUT_PATH',
     'Z1_LEVEL',
     'Z2_LEVEL']




```python
inspect.ismethod(getattr(dr,i))
```




    True




```python

```
