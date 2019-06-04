# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

import datetime
import os

import pandas as pd

RELEASE_DIC_STR_KEY = 'release_dic_str'

END_DT_REL_KEY = 'end_dt_rel'
START_DT_REL_KEY = 'start_dt_rel'
RELEASE_NAME_KEY = 'release_name'

RELEASE_TEMP = '''  {start_dt_rel}       ID1, IT1        beginning date and time of release
  {end_dt_rel}       ID2, IT2        ending date and time of release
  -68.140000            XPOINT1 (real)  longitude [deg] of lower left corner
  -16.355000            YPOINT1 (real)  latitude [deg] of lower left corner
  -68.118000            XPOINT2 (real)  longitude [deg] of upper right corner
  -16.335000            YPOINT2 (real)  latitude [DEG] of upper right corner
  1                     KINDZ  (int)  1 for m above ground, 2 for m above sea level, 3 pressure
  {z1_level:0.1f}                 ZPOINT1 (real)  lower z-level
  {z2_level:0.1f}                ZPOINT2 (real)  upper z-level
  {n_particles:0.0f}                 NPART (int)     total number of particles to be released
  {mass_emmitted:0.1f}                XMASS (real)    total mass emitted
  {release_name}    NAME OF RELEASE LOCATION'''

# @formatter:off

RELEASE_DEFAULT_DICT = dict(
    start_dt_rel	    =	datetime.datetime(2017,12,9,23,0,0) 		    ,
    end_dt_rel	        =	datetime.datetime(2017,12,10,0,0,0) 	        ,
    z1_level			=	0.0                                 			,
    z2_level			=	10.00                               			,
    n_particles			=	10000                               			,
    mass_emmitted		= 	1000.0                              			,
    release_name        =   'dummy_test'                                 ,
)
# @formatter:on


def format_release_template(release_dict: dict = {}) -> str:
    combined_release_dic = RELEASE_DEFAULT_DICT
    for k, v in release_dict.items():
        combined_release_dic[k] = v
    combined_release_dic = format_release_dict(combined_release_dic)
    formatted_release_str = RELEASE_TEMP.format(**combined_release_dic)
    return formatted_release_str


def format_dt_to_str(dt: datetime.datetime) -> str:
    return dt.strftime('%Y%m%d %H%M%S')


def format_release_dict(rel_dic: dict) -> dict:
    dt_keys = [START_DT_REL_KEY, END_DT_REL_KEY]
    for k in dt_keys:
        check = type(rel_dic[k])
        if (check == datetime.datetime) or (check == pd.Timestamp):
            rel_dic[k] = format_dt_to_str(rel_dic[k])
    return rel_dic


def create_dic_range(*,
                     d_start: datetime.datetime,
                     d_end: datetime.datetime,
                     base_dict: dict,
                     h_frq: int = 1,
                     ) -> pd.DataFrame:
    join_dict = RELEASE_DEFAULT_DICT
    for k, v in base_dict.items():
        join_dict[k] = v
    dt_index: pd.DatetimeIndex = pd.date_range(d_start, d_end, freq='{}H'.format(h_frq))
    df = pd.DataFrame(dt_index, columns=[START_DT_REL_KEY])[:]
    delta_h = pd.Timedelta(h_frq, 'H')
    df[END_DT_REL_KEY] = df[START_DT_REL_KEY] + delta_h
    base_rel_name = join_dict[RELEASE_NAME_KEY]
    pat = '{}%Y%m%d_%H'.format(base_rel_name)
    df[RELEASE_NAME_KEY] = df[START_DT_REL_KEY].dt.strftime(pat)
    rel_dic_un_key = 'release_dic_unformatted'
    rel_dic_for_key = 'release_dic_formatted'
    df[rel_dic_un_key] = df.apply(lambda r: {**base_dict, **r}, axis=1)
    df[rel_dic_for_key] = df.apply(lambda r: format_release_dict(r[rel_dic_un_key]), axis=1)
    df[RELEASE_DIC_STR_KEY] = df[rel_dic_for_key].apply(lambda v: format_release_template(v))
    return df


def get_release_temp_str_from_df(df: pd.DataFrame):
    st = df[RELEASE_DIC_STR_KEY].values
    str_out = ''
    for s in st:
        str_out = str_out + '\n' + s
    str_out = str_out[1:]
    return str_out


def get_release_temp_str(
        d_start: datetime.datetime,
        d_end: datetime.datetime,
        z1_level: float,
        z2_level: float,
        n_particles: int,
        mass_emmitted: float,
        release_name: str,
        release_frq:int,
) -> str:
    base_dict = dict(
        z1_level=z1_level,
        z2_level=z2_level,
        n_particles=n_particles,
        mass_emmitted=mass_emmitted,
        release_name=release_name,
    )
    df = create_dic_range(
        d_start=d_start,
        d_end=d_end,
        base_dict= base_dict,
        h_frq = release_frq
    )
    rel_str = get_release_temp_str_from_df(df)
    return rel_str


AVAIL_HEAD_TEMP = """XXXXXX EMPTY LINES XXXXXXXXX
XXXXXX EMPTY LINES XXXXXXXX
YYYYMMDD HHMMSS   name of the file(up to 80 characters)"""

AVAIL_ROW_TEMP = """{exact_date}      'wrfout_d{dom00}_{file_date}'      ' '"""


def get_avail_str(d1, d2, dom00, frq_file=60, frq_sim=15):
    d2_plus_1 = d2 + datetime.timedelta(minutes=frq_file)
    date_range = pd.date_range(d1, d2_plus_1,
                               freq='{}min'.format(frq_sim),
                               closed='left')
    frq_sim_key = 'frq_sim'
    file_dt_key = 'file_dt'
    df = pd.DataFrame(date_range, columns=[frq_sim_key])
    df[file_dt_key] = df[frq_sim_key].dt.floor('{}min'.format(frq_file))
    for_sim = '%Y%m%d %H%M%S'
    for_file = '%Y-%m-%d_%H:%M:%S'
    file_frtted_key = 'file_date'
    sim_time_frtted_key = 'exact_date'
    dom_key = 'dom00'
    df[file_frtted_key] = df[file_dt_key].dt.strftime(for_file)
    df[sim_time_frtted_key] = df[frq_sim_key].dt.strftime(for_sim)
    df[dom_key] = dom00
    str_key = 'row_str'
    df[str_key] = df.apply(lambda r: AVAIL_ROW_TEMP.format(**r), axis=1)

    str_out = AVAIL_HEAD_TEMP
    for s in df[str_key].values:
        str_out = str_out + '\n' + s

    return str_out


def create_avail_file(d1, d2, dom00, frq_file=60, frq_sim=15,
                      output_dir='/tmp/', file_base_name='AVAILABLE'):
    out_str = get_avail_str(d1, d2, dom00, frq_file, frq_sim)
    file_name = file_base_name + dom00
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'w') as file:
        file.write(out_str)
    return True


def create_all_avail_files(d1, d2, doms00=['01', '02', '03', '04'],
                           frq_file=60, frq_sim=15,
                           output_dir='/tmp/',
                           file_base_name='AVAILABLE'):
    for d in doms00:
        create_avail_file(d1, d2, d, frq_file, frq_sim, output_dir, file_base_name)
