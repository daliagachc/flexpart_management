# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import datetime as dt
import flexpart_management.modules.daily_back.ConfigDayRun as CDR


class DayRun(CDR.ConfigDayRun):
    DATE_SIMULATION         =   dt.date(2017,12,10)
    HOURS_BACK_IN_TIME      =   96   # possitive
    RUN_BASE_NAME           =   'run_2019-06-02_20-42-05_'
    RUN_BASE_PATH           =   '/tmp/'
    RUN_BASE_PATH_TAITO     =   '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/'
    WRFOUT_PATH             =   '/proj/atm/saltena/runs/run_2019_05_15/wrf'
    FLX_INPUT_TEMPL_PATH    =   '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/flex_input_templ'
    RUN_TEMPL_PATH          =   '/Users/diego/flexpart_management/flexpart_management/modules/daily_back/run_flex_templ.sh'
    Z1_LEVEL                =   0.0
    Z2_LEVEL                =   10.0
    N_PARTICLES             =   100000
    MASS_EMMITTED           =   1.0
    RELEASE_NAME            =   'chc' # release base nameo
    FLX_EXE                 =   'flexwrf33_gnu_omp'
    SBATCH_N:int            = 2
    SBATCH_T:str            = '02:00:00'
    SBATCH_P:str            = 'parallel'
    SBATCH_M:int            = 8000
    FLX_EXE: str            = 'flexwrf33_gnu_omp'