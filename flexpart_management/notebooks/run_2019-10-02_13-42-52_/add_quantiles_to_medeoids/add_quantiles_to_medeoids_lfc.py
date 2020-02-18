# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import *
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
import weightedcalcs as wc
from sqlalchemy import create_engine

# noinspection PyStatementEffect,PyTrailingSemicolon
co, fa, plt;
# %%
def get_weighted_stats(da, dim_to_calc,
                       sum_before=True, roll=False,mean_rad_i = None
                       )->dict:
    # dal = da.where(da['lab'] == lab)
    dal =da
    if sum_before:
        com_dim = fa.get_dims_complement(dal, dim_to_calc)
        d1 = dal.sum(com_dim)
    else:
        d1 = dal
    df = d1.to_dataframe()
    # print(df)
    # return
    df = df.reset_index()[[co.CONC,dim_to_calc]]
    wei = wc.Calculator(co.CONC)
    # print(df)
    df_bg_0 = df[co.CONC].sum()>0

    if df_bg_0:
        res_dic = dict(
            med=wei.median(df, dim_to_calc),
            avg=wei.mean(df, dim_to_calc),
            std=wei.std(df, dim_to_calc),
            q05=wei.quantile(df, dim_to_calc, 0.05),
            q95=wei.quantile(df, dim_to_calc, 0.95),
            q25=wei.quantile(df, dim_to_calc, 0.25),
            q75=wei.quantile(df, dim_to_calc, 0.75),
            val=wei.sum(df, dim_to_calc)
        )
        if roll:
            for k,v in res_dic.items():
                val = v + (mean_rad_i * np.pi / 18)
                val = np.mod(val,2 * np.pi)
                res_dic[k] = val
    else:
        res_dic = dict(
            med=np.nan,
            avg=np.nan,
            std=np.nan,
            q05=np.nan,
            q95=np.nan,
            q25=np.nan,
            q75=np.nan,
            val=np.nan,
        )

    return res_dic

# %%
def get_weighted_stats_rl(da_con, dim_to_calc, lab, echo=False,
                          sum_before=True, roll=False):
    da_con_lab = da_con.where(da_con['lab'] == lab)
    dic = {}
    for rl in da_con_lab[co.RL]:
        datetime = pd.to_datetime(rl.item())
        if echo:
            print(datetime)
        da = da_con_lab.loc[{co.RL: rl}]
        mean_rad_i = None
        if roll:
            da,mean_rad_i = roll_th(da)
        dic[datetime] = get_weighted_stats(
            da, dim_to_calc,sum_before=sum_before,
            roll = roll, mean_rad_i=mean_rad_i
        )
    df = pd.DataFrame(dic).T
    df.index.name=co.RL
    df.T.index.name = dim_to_calc
    xa:xr.Dataset = df.to_xarray()
    # noinspection PyTypeChecker
    xa = xa.to_array(name=dim_to_calc, dim='stat')
    xa = xa.expand_dims(dim={'lab':[lab]})
    return xa
# %%
def get_stats(da_con, labs, type1, type):
    type_dic = dict(
        z_r = dict(roll=False, sum_before=True),
        z_ag=dict(roll=False, sum_before=False),
        th=dict(roll=True, sum_before=True),
    )
    ls_xa = []
    for lab in labs:
        for dim_to_calc in type1:
            # dim_to_calc = co.ZM
            xa = get_weighted_stats_rl(da_con, dim_to_calc, lab,
                                       **type_dic[type])
            ls_xa.append(xa)
    xa_mer = xr.merge(ls_xa)
    return xa_mer
# %%
def roll_th(da_con_lab_first:xr.DataArray):
    da_con_lab = da_con_lab_first.sum([co.ZM, co.R_CENTER])
    x = da_con_lab * np.cos(da_con_lab[co.TH_CENTER])
    y = da_con_lab * np.sin(da_con_lab[co.TH_CENTER])
    mean_rad = np.arctan2(y.sum(), x.sum())
    mean_rad_i = int(mean_rad / (np.pi / 18)) + 18
    da_roll = da_con_lab_first.roll(**{co.TH_CENTER: -mean_rad_i},roll_coords=True)
    return da_roll, mean_rad_i

# %%
sql_path = 'sqlite:////Users/diego/flexpart_management/flexpart_management/notebooks/run_2019-10-02_13-42-52_/add_quantiles_to_medeoids/add_quantiles_to_medeoids.sqlite'
# %%
def create_db(ds, tab_name, drop_if_exists=False):
    tm_df: pd.DataFrame = ds[co.RL].to_dataframe().reset_index(drop=True)
    tm_df['ran'] = False
    tm_df['running'] = False
    _dt = tm_df[co.RL].dt
    tm_df['file_name'] = _dt.strftime('%Y-%m-%d_%H.nc')
    engine = get_engine()
    if drop_if_exists:
        engine.execute(f'drop table if exists {tab_name}')
    try:
        tm_df.to_sql(tab_name, engine)
    except:
        log.ger.warning('table exists so not created')

    engine.execute(f'update {tab_name} set running=0 where ran=0')
    return engine


def get_engine():
    engine = create_engine(sql_path, echo=False)
    return engine


# %%
def get_last_row(engine, tab_name):
    sql = f'select * from {tab_name} where ran=0 and running=0 limit 1'
    open_tab = pd.read_sql(sql, engine, index_col='index', parse_dates=co.RL)
    row = open_tab.iloc[0]
    engine.execute(f'update {tab_name} set running=1 where `index`={row.name}')
    return row

# %%
def update_tab_success(engine, row, tab_name):
    engine.execute(f'update `{tab_name}` set ran=1 where {row.name}=`index`')

# %%
def get_the_stats(da_load, row):
    da_con = da_load.loc[{co.RL: [row[co.RL]]}]

    da_con_ag = da_con.assign_coords({'Z_AG': da_con[co.ZM] - da_con[co.TOPO]})
    labs = range(18)
    type1 = [co.ZM, co.R_CENTER]
    xa_mer = get_stats(da_con_ag, labs, type1, type='z_r')
    xa_mer1 = get_stats(da_con_ag, labs, ['Z_AG'], type='z_ag')
    xa_mer2 = get_stats(da_con_ag, labs, [co.TH_CENTER], type='th')
    mega_ds = xr.merge([xa_mer, xa_mer1, xa_mer2])
    mega_ds = mega_ds.rename({co.ZM: 'ZMID_ASL', 'Z_AG': 'ZMID_AGL'})
    return mega_ds

# %%
def save_the_multiple_files(path_out, tab_name, tmp_dir):
    engine = get_engine()
    sql = f'select * from {tab_name} where ran=1'
    df = pd.read_sql(sql, engine)
    df['path'] = tmp_dir + '/' + df['file_name']
    mds = xr.open_mfdataset(df['path'], concat_dim=co.RL, combine='nested')
    # %%
    mds.to_netcdf(path_out)

# %%

def open_clus_ts():
    clus_ts = pd.read_csv(pjoin(co.tmp_data_path, 'conc_ts_cluster.csv'))
    clus_ts = clus_ts.set_index(co.RL)
    return clus_ts


def open_prop_df():
    prop_df = pd.read_csv(
        pjoin(co.tmp_data_path, 'prop_df_.csv'),
        index_col='cluster_i'
    )
    if 'hgk_xy' in prop_df.columns:
        prop_df = prop_df.drop('hgk_xy', axis=1)
    return prop_df

# %%
# %%
# %%
# %%
# %%

