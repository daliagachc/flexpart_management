# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import datetime as dt
import os
import flexpart_management.modules.daily_back.daily_back as db
import pandas as pd
import subprocess
from pprint import pprint

# @formatter:off
class ConfigDayRun:
    DATE_SIMULATION:dt.date         = None
    HOURS_BACK_IN_TIME:int          = None
    RUN_BASE_NAME:str               = None
    RUN_BASE_PATH:str               = None
    RUN_BASE_PATH_TAITO:str         = None
    WRFOUT_PATH:str                 = None
    FLX_INPUT_TEMPL_PATH:str        = None
    RUN_TEMPL_PATH:str              = None
    RUN_PATH:str                    = None
    RUN_PATH_TAITO:str              = None
    DAY_PATH:str                    = None
    DAY_PATH_TAITO:str              = None
    DT_END_SIMULATION:dt.datetime   = None
    DT_START_SIMULATION:dt.datetime = None
    DT_FIRST_RELEASE:dt.datetime    = None
    DT_LAST_RELEASE:dt.datetime     = None
    DOMAINS                         = ['01','02','03','04']
    RELEASE_STR:str                 = None
    Z1_LEVEL:float                  = None
    Z2_LEVEL:float                  = None
    N_PARTICLES:int                 = None
    MASS_EMMITTED:float             = None
    RELEASE_NAME:str                = None # release base name
    RELEASE_FRQ:int                 = 1
    AVAILABLE_FILE_BASE_NAME:str    = 'AVAILABLE'
    FRQ_WRFOUT_FILES_M:int          = 60
    FRQ_SIMULATION_M:int            = 15
    NUMBER_OF_RELEASES:int          = 24
    AVAILABLE_PATHS: list           = None
    INPUT_TEMPL_STR: str            = None
    FLX_INPUT_PATH: str             = None
    FLX_INPUT_PATH_TAITO: str       = None
    FLX_INPUT_BASE_NAME: str        = 'flx_input'
    SBATCH_N:int                    = 2
    SBATCH_T:str                    = '02:00:00'
    SBATCH_P:str                    = 'parallel'
    SBATCH_M:int                    = 8000
    FLX_EXE: str                    = 'flexwrf33_gnu_omp'
    RUN_FLX_BASE_NAME: str          = 'run_flex.sh'
    RUN_FLX_TEST_BASE_NAME: str     = 'run_flex_test.sh'
    RUN_FLX_PATH: str               = None
    RUN_FLX_PATH_TAITO: str         = None
    RUN_FLX_PATH_TEST: str          = None
    RUN_FLX_PATH_TEST_TAITO: str    = None



# @formatter:on
    def generate_run_path(self) -> None:
        self.RUN_PATH = os.path.join(self.RUN_BASE_PATH,
                                     self.RUN_BASE_NAME)
        self.RUN_PATH_TAITO = os.path.join(self.RUN_BASE_PATH_TAITO,
                                           self.RUN_BASE_NAME)

    def generate_day_path(self) -> None:
        day_str = self.DATE_SIMULATION.strftime('%Y-%m-%d')
        self.DAY_PATH = os.path.join(self.RUN_PATH, day_str)
        self.DAY_PATH_TAITO = os.path.join(self.RUN_PATH_TAITO, day_str)

    def get_dt_end_simulation(self) -> None:
        dt_end = dt.datetime(*self.DATE_SIMULATION.timetuple()[:6])
        dt_end = dt_end + dt.timedelta(hours=self.NUMBER_OF_RELEASES)
        self.DT_END_SIMULATION = dt_end

    def get_dt_start_simulation(self) -> None:
        dt_start = dt.datetime(*self.DATE_SIMULATION.timetuple()[:6])
        dt_start = dt_start - dt.timedelta(hours=self.HOURS_BACK_IN_TIME)
        self.DT_START_SIMULATION = dt_start

    def get_dt_first_release(self) -> None:
        dt_rel = dt.datetime(*self.DATE_SIMULATION.timetuple()[:6])
        self.DT_FIRST_RELEASE = dt_rel

    def get_dt_last_release(self) -> None:
        dt_rel = dt.datetime(*self.DATE_SIMULATION.timetuple()[:6])
        dt_rel = dt_rel + dt.timedelta(hours=self.NUMBER_OF_RELEASES - self.RELEASE_FRQ)
        self.DT_LAST_RELEASE = dt_rel

    def get_release_str(self) -> None:
        self.RELEASE_STR = db.get_release_temp_str(
            self.DT_FIRST_RELEASE,
            self.DT_LAST_RELEASE,
            self.Z1_LEVEL,
            self.Z2_LEVEL,
            self.N_PARTICLES,
            self.MASS_EMMITTED,
            self.RELEASE_NAME,
            self.RELEASE_FRQ
        )

    def create_day_path_dir(self):
        os.makedirs(self.DAY_PATH, exist_ok=True)

    def create_available_files(self) -> None:
        db.create_all_avail_files(
            self.DT_START_SIMULATION,
            self.DT_END_SIMULATION,
            self.DOMAINS,
            self.FRQ_WRFOUT_FILES_M,
            self.FRQ_SIMULATION_M,
            self.DAY_PATH,
            self.AVAILABLE_FILE_BASE_NAME
        )

    def create_available_paths(self) -> None:
        avail_paths = []
        for d in self.DOMAINS:
            path = os.path.join(self.DAY_PATH_TAITO,
                                self.AVAILABLE_FILE_BASE_NAME + d)
            avail_paths.append(path)
        self.AVAILABLE_PATHS = avail_paths

    def get_input_templ_string(self):
        with open(self.FLX_INPUT_TEMPL_PATH, 'r') as file:
            string = file.read()
        self.INPUT_TEMPL_STR = string

    def fill_out_templ_string(self):
        wrfout_path = os.path.join(self.WRFOUT_PATH, '')
        day_path = os.path.join(self.DAY_PATH_TAITO, '')
        wrfout_path_avail_file = ''
        for ap in self.AVAILABLE_PATHS:
            wrfout_path_avail_file = wrfout_path_avail_file + \
                                     wrfout_path + '\n' + \
                                     ap + '\n'
        wrfout_path_avail_file = wrfout_path_avail_file[:-1]

        d1 = db.format_dt_to_str(self.DT_START_SIMULATION)
        d2 = db.format_dt_to_str(self.DT_END_SIMULATION)

        fill_dic = dict(
            wrfout_path_avail_file=wrfout_path_avail_file,
            path_simulation=day_path,
            number_of_releases=self.NUMBER_OF_RELEASES,
            releases_string=self.RELEASE_STR,
            date_start_simulation_format=d1,
            date_end_simulation_format=d2,
            age_length_secs=self.HOURS_BACK_IN_TIME * 3600,
        )

        self.INPUT_TEMPL_STR = self.INPUT_TEMPL_STR.format(**fill_dic)

    def create_flx_input_path(self):
        self.FLX_INPUT_PATH = os.path.join(self.DAY_PATH,
                                           self.FLX_INPUT_BASE_NAME)
        self.FLX_INPUT_PATH_TAITO = os.path.join(self.DAY_PATH_TAITO,
                                                 self.FLX_INPUT_BASE_NAME)

    def create_flx_input_file(self):
        with open(self.FLX_INPUT_PATH, 'w') as file:
            file.write(self.INPUT_TEMPL_STR)

    def create_run_flx_path(self):
        self.RUN_FLX_PATH = os.path.join(self.DAY_PATH,
                                         self.RUN_FLX_BASE_NAME)
        self.RUN_FLX_PATH_TAITO = os.path.join(self.DAY_PATH_TAITO,
                                               self.RUN_FLX_BASE_NAME)
        self.RUN_FLX_PATH_TEST = os.path.join(self.DAY_PATH,
                                              self.RUN_FLX_TEST_BASE_NAME)
        self.RUN_FLX_PATH_TEST_TAITO = os.path.join(self.DAY_PATH_TAITO,
                                                    self.RUN_FLX_TEST_BASE_NAME)

    def fill_out_run_flx(self):
        with open(self.RUN_TEMPL_PATH, 'r') as file:
            string = file.read()

        fill_dic = dict(
            SBATCH_N=self.SBATCH_N,
            SBATCH_T=self.SBATCH_T,
            SBATCH_P=self.SBATCH_P,
            SBATCH_M=self.SBATCH_M,
            FLX_INPUT_PATH_TAITO=self.FLX_INPUT_PATH_TAITO,
            FLX_EXE=self.FLX_EXE,
        )

        string_out = string.format(**fill_dic)

        file = open(self.RUN_FLX_PATH, 'w')
        file.write(string_out)
        file.close()

        fill_dic['SBATCH_P'] = 'test'
        fill_dic['SBATCH_T'] = '00:30:00'
        string_out = string.format(**fill_dic)
        file = open(self.RUN_FLX_PATH_TEST, 'w')
        file.write(string_out)
        file.close()

    def get_class_dict(self) -> dict:
        import inspect
        variables = []
        for i in dir(self):
            try:
                if not inspect.ismethod(getattr(self, i)):
                    if i[:1] is not '_':
                        variables.append(i)
            except:
                pass
        dic = {}
        for v in variables:
            dic[v] = getattr(self, v)
        return dic

    def __init__(self, init_dic={}):
        if init_dic == {}:
            print('dict empty')
        else:
            for k, v in init_dic.items():
                setattr(self, k, v)

        self.generate_run_path()
        self.generate_day_path()
        self.get_dt_end_simulation()
        self.get_dt_start_simulation()
        self.get_dt_first_release()
        self.get_dt_last_release()
        self.get_release_str()
        self.create_day_path_dir()
        self.create_available_files()
        self.create_available_paths()
        self.get_input_templ_string()
        self.fill_out_templ_string()
        self.create_flx_input_path()
        self.create_flx_input_file()
        self.create_run_flx_path()
        self.fill_out_run_flx()



class ConfigMultiDayRun:
    DATE_START: dt.date = None
    DATE_END: dt.date = None
    DATE_RANGE: pd.DatetimeIndex = None
    EXCEPTS = ('DATE_START','DATE_END')
    INIT_DIC:dict = None
    DICS_FOR_DAY_RUN:list = []
    RUN_PATH_LOCAL_RSYNC = ''
    RUN_PATH_TAITO_RSYNC = ''

    def set_date_range(self):
        dr = pd.date_range(self.DATE_START,
                           self.DATE_END,
                           freq='D')
        dr = dr.to_pydatetime()
        self.DATE_RANGE = dr
    def pop_init_dic(self):
        init_dict = self.INIT_DIC.copy()
        for k in self.EXCEPTS:
            init_dict.pop(k,None)
        self.INIT_DIC=init_dict

    def set_dics_for_day_run(self):
        dics = []
        for d in self.DATE_RANGE:
            print(d)
            dic = self.INIT_DIC.copy()
            dic['DATE_SIMULATION'] = d
            dics.append(dic)
        self.DICS_FOR_DAY_RUN = dics

    def create_daily_runs(self):
        for d in self.DICS_FOR_DAY_RUN:
            ConfigDayRun(init_dic=d)

    def rsync_to_taito(self):
        list_cmds = [
            '/usr/local/bin/rsync',
            '-azv',
            self.RUN_PATH_LOCAL_RSYNC,
            'aliagadi@taito-login3.csc.fi:' + \
            self.RUN_PATH_TAITO_RSYNC
        ]
        pprint(list_cmds)
        subprocess.call(list_cmds)



    def __init__(self,
                 init_dic = {}):
        print(init_dic)
        self.INIT_DIC = init_dic
        self.DATE_START = init_dic['DATE_START']
        self.DATE_END = init_dic['DATE_END']
        print(self.DATE_END)
        self.set_date_range()
        self.pop_init_dic()
        self.set_dics_for_day_run()
        self.create_daily_runs()
        self.RUN_PATH_LOCAL_RSYNC = os.path.join(
            self.INIT_DIC['RUN_BASE_PATH'],
            self.INIT_DIC['RUN_BASE_NAME'],
            '' # ensure trailing space
        )
        self.RUN_PATH_TAITO_RSYNC = os.path.join(
            self.INIT_DIC['RUN_BASE_PATH_TAITO'],
            self.INIT_DIC['RUN_BASE_NAME'],
            '' # ensure trailing space
        )
