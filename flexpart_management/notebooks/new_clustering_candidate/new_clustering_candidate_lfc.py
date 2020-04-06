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
import os

from useful_scit.imps import *
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co
from sqlalchemy import create_engine
import sqlalchemy
from useful_scit.imps import pjoin
from useful_scit.util import log

TAB_NAME1 = 'ss_data'

plt;
# %%
def update_ss(engine, r,
              ss,inertia,db_index,ch_index,
              TAB_NAME):
    engine:sqlalchemy.engine.base.Engine
    query_update = f'''
    update {TAB_NAME} 
    set 
    n_ss={ss},
    inertia={inertia},
    db_index={db_index},
    ch_index={ch_index}
    where `index`={r.name}'''
    with engine.connect() as con:
        con.execute(query_update)


def get_silhouette(das3, r):
    from sklearn.cluster import KMeans,MiniBatchKMeans
    if r['n_cl']>30:
        fun = MiniBatchKMeans
    else:
        fun = KMeans
    # dd = dat[{'stack':slice(0,None)}]
    k_means = fun(
        n_clusters=r['n_cl'],
        n_init=10,
        random_state=r['rnds'],
    )
    vals_ = das3[r['norm']]
    res = k_means.fit(vals_, sample_weight=das3['weight'])
    from sklearn.metrics import silhouette_score, silhouette_samples, davies_bouldin_score, calinski_harabasz_score
    labs_ = res.predict(vals_)
    ss = silhouette_samples(vals_, labs_)
    ss = (ss * das3['weight']).sum() / das3['weight'].sum()
    ss = ss.item()
    log.ger.debug('ss is %s',ss)

    inertia = k_means.inertia_
    db_index = davies_bouldin_score(vals_, labs_)
    ch_index = calinski_harabasz_score(vals_,labs_)


    return ss,inertia,db_index,ch_index


def get_next_row(engine, TAB_NAME):
    rnd_query = f'select * from {TAB_NAME} where n_ss=0 order by random() limit 1'
    rows = pd.read_sql(rnd_query, con=engine, index_col='index')
    if len(rows) is 1:
        r = rows.iloc[0]
    else:
        r = False
    return r


def create_res_db(engine, TAB_NAME, force_create=False, min_cl=2, max_cl=25, int_cl=1,
                  rnds_len=22):
    if check_if_tab_exist(engine, TAB_NAME):
        log.ger.warn('table exists')
        if force_create:
            log.ger.warn('recreating tab')
        else:
            return False

    norm_vals = ['qua_tra', 'pow_tra', 'sta_sca', 'nor_sca']
    n_ss_vals = [0.0]
    n_cl_vals = np.arange(min_cl, max_cl, int_cl)
    rnds_vals = np.arange(1, rnds_len, 1)
    tab_dic = {
        'norm': {'vals': norm_vals},
        'n_ss': {'vals': n_ss_vals},
        'n_cl': {'vals': n_cl_vals},
        'rnds': {'vals': rnds_vals},
    }
    # %%
    from itertools import product
    df = pd.DataFrame(tab_dic)
    uniques = [df[i]['vals'] for i in df.columns]
    df = pd.DataFrame(product(*uniques), columns=df.columns)
    df['inertia'] = 0.0
    df['db_index'] = 0.0
    df['ch_index'] = 0.0
    # %%
    # %%
    df.to_sql(TAB_NAME, con=engine, )
    return True


def preprocess(das):
    import sklearn.preprocessing
    qua_tra = sklearn.preprocessing.QuantileTransformer
    qua_tra_par = {}
    pow_tra = sklearn.preprocessing.PowerTransformer
    pow_tra_par = {
        'standardize': False
    }
    sta_sca = sklearn.preprocessing.StandardScaler
    sta_sca_par = {'with_mean': False}
    nor_sca = sklearn.preprocessing.Normalizer
    nor_sca_par = {'norm': 'l2'}
    rob_sca = sklearn.preprocessing.RobustScaler
    rob_sca_par = {'with_centering': False, 'quantile_range': (0, 75)}
    pre_dic = dict(
        qua_tra={'tra': qua_tra, 'par': qua_tra_par},
        pow_tra={'tra': pow_tra, 'par': pow_tra_par},
        sta_sca={'tra': sta_sca, 'par': sta_sca_par},
        nor_sca={'tra': nor_sca, 'par': nor_sca_par},
        # rob_sca={'tra': rob_sca, 'par': rob_sca_par},
    )
    # %%
    das2 = das[{'stack': das['above_thre']}]
    # das2 =das2[{'stack':slice(0,10)}]
    das2 = das2.transpose(co.RL, 'stack')
    _weight = das2.sum(co.RL)
    das2 = das2.assign_coords({'weight': _weight})
    # %%
    das3 = das2
    for l, v in pre_dic.items():
        tra = v['tra']
        par = v['par']
        res = tra(**par).fit_transform(das2)
        ones = xr.ones_like(das2) * res
        ones.name = l
        das3 = xr.merge([das3, ones])

    das3 = das3.transpose('stack',co.RL)
    return das3


def load_data():
    ds = fa.open_temp_ds_clustered_18()
    cs = 'CONC_smooth_t_300_z_25_r_100_th_50'
    da = ds[cs]
    da: xr.DataArray = da[:, :, :, :]
    das = da.stack({'stack': [co.R_CENTER, co.TH_CENTER, co.ZM]})
    das = das[{'stack': slice(0, None, 1)}]
    das.load()
    return das

def check_if_tab_exist(engine, TAB_NAME):
    sql = f'''
    SELECT name FROM sqlite_master WHERE type='table' AND name="{TAB_NAME}"
    '''

    df = pd.read_sql(sql,con=engine)

    res=False
    if len(df) is 1:
        res = True

    return res


def script_find_ss(nb_dir,
                   min_cl=50, max_cl=100, int_cl=10, rnds_len=2, tab_name='ss_data_long_long'):
    # %%
    log.ger.setLevel(log.log.DEBUG)
    # %%
    process_file_path = pjoin(co.tmp_data_path,'ds_clustered_18_with_mult_norms.nc')
    log.ger.debug('tmp path is %s',process_file_path)

    process_file_exists = os.path.isfile(process_file_path)


    # %%
    TAB_NAME = tab_name
    if process_file_exists is False:
    # if True:
        log.ger.debug('load data')
        das = load_data()
        log.ger.debug('preprocess')
        das3 = preprocess(das)
        log.ger.debug('save compressing %s','')
        das3u = das3.unstack('stack')
        fa.compressed_netcdf_save(das3u,process_file_path)
        # TODO: the saving doesnt workd due to multindex in
        # in the array
    #     i think is solved now
    else:
        das3u = xr.open_mfdataset(process_file_path, combine='nested',
                                 concat_dim=co.RL)
        das3 = das3u.stack(stack=[co.ZM,co.TH_CENTER,co.R_CENTER])
        das3 = das3.dropna('stack')
        das3 = das3.transpose('stack', co.RL)


    # %%
    sql_path = 'sqlite:///'+pjoin(nb_dir,TAB_NAME+'.db')
    # %%

    engine = create_engine(sql_path, echo=False)
    # %%

    create_res_db(engine, TAB_NAME=TAB_NAME, min_cl=min_cl, max_cl=max_cl, int_cl=int_cl, rnds_len=rnds_len)

    # %%
    while True:
        r = get_next_row(engine,TAB_NAME)
        log.ger.debug('doing r %s',r)
        if r is False:
            break

        ss, inertia, db_index, ch_index = get_silhouette(das3, r)
        try: update_ss(engine, r, ss,inertia,db_index,ch_index, TAB_NAME)
        except:
            try: update_ss(engine, r,ss,inertia,db_index,ch_index, TAB_NAME)
            except: pass

    # %%
    # %%
    log.ger.debug('nothin else to do :)')

def get_df(nb_dir, tab_name='ss_data_long'):
    sql_path = 'sqlite:///' + pjoin(nb_dir, tab_name + '.db')
    engine = create_engine(sql_path, echo=False)
    df = pd.read_sql(tab_name, con=engine)
    df1 = df[df['n_ss'] > 0]
    return df1

def plot_score(nb_dir, score_par='n_ss'):
    tabs = ['ss_data_l',
            # 'ss_data_ll', 'ss_data_lll', 'ss_data_llll'
            ]
    ls = []
    for t in tabs:
        try:
            df1 = get_df(nb_dir, tab_name=t)
            ls.append(df1)
        except:
            pass
    df = pd.concat(ls)
    # sns.swarmplot(x='n_cl',y='n_ss',hue='norm',data=df)
    # sns.stripplot(x='n_cl',y='n_ss',hue='norm',data=df)
    f, ax = plt.subplots(figsize=(7.25, 7.25 / 1.6), dpi=300)
    ax: plt.Axes
    p_dic = dict(
        pow_tra={'c': ucp.cc[0], 'y': 0.270, 'name': 'power\ntransform'},
        qua_tra={'c': ucp.cc[1], 'y': 0.170, 'name': 'quantile\ntransform'},
        nor_sca={'c': ucp.cc[2], 'y': 0.145, 'name': 'norm\nscaler'},
        sta_sca={'c': ucp.cc[3], 'y': 0.105, 'name': 'standard\nscaler'},
    )
    p_dic = pd.DataFrame(p_dic).T
    for l, r in p_dic.iterrows():
        # ax.annotate(r['name'], xy=[2, r['y']], color=r['c'])
        pass
    par = score_par

    g = sns.FacetGrid(data=df,row='norm',hue='norm',sharey=False,
                      palette=p_dic['c'].to_dict(),
                      aspect=2
                      )
    # sns.scatterplot(x='n_cl', y=par, hue='norm', data=df, ax=ax,
    #                 s=10, palette=p_dic['c'].to_dict(),
    #                 # edgecolor='none',
    #                 linewidth=.2,
    #                 alpha=.5
    #                 )
    g.map(sns.scatterplot,'n_cl',par)

    df1 = df.groupby(['norm', 'n_cl']).max()[par].reset_index()

    # sns.lineplot(x='n_cl', y=par, hue='norm', data=df1, ax=ax,
    #              palette=p_dic['c'].to_dict())


    ax.set_xticks([10, 100, 1000])
    ax.set_xticklabels([10, 100, 1000])
    xmt = []
    for i in [2, 3, 4, 5, 6, 7, 8, 9]:
        for ii in [1, 10, 100]:
            xmt.append(i * ii)
    _df = pd.DataFrame(xmt, columns=['t']).set_index('t')
    _df['s'] = None
    _df.loc[2, 's'] = 2
    _df.loc[20, 's'] = 20
    _df.loc[400, 's'] = 400
    # ax.set_xticks(_df.index, minor=True)
    # ax.set_xticklabels(_df['s'], minor=True, fontdict={'fontsize': 6})
    # ax.set_yticks([.1, .2, .3, .4, .5])
    # ax.set_yticklabels([.1, .2, .3, .4, .5])
    ax.set_xlabel('number of clusters')
    # ax.set_ylabel('Silhouette average score')
    ax.set_ylabel(score_par)
    # ax.legend(loc='lower right')
    # ax.get_legend().remove()
    # ax.set(xscale='log', yscale='log')
    ax.set_xlim(1, 30)
    # ax.set_ylim(.05, .3)
    _b1 = df1['norm'] == 'qua_tra'
    _b2 = df1['n_cl'] == 18
    # _y = df1[_b1 & _b2]['n_ss'].item()
    # # TODO: fix stuff here
    # ax.annotate('18th clusters',
    #             xy=[18,_y],
    #             xytext=[0,20],
    #             textcoords='offset points',
    #             arrowprops={'arrowstyle':'->'},
    #             horizontalalignment='right'
    #             )
    plt.show()
