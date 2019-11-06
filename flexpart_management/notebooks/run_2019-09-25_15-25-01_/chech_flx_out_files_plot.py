# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import (pd,np,xr,za,mpl,plt,sns, pjoin, os,glob,dt,
    sys,ucp,log, splot, crt,axsplot)
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

# %%
path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/'+\
'runs/run_2019-09-25_15-25-01_/*-*-*/flx*.nc'
PATH_OUT = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/'+\
'runs/run_2019-09-25_15-25-01_/check_plots'

# %%

# %%
os.mkdir(PATH_OUT)

# %%
ls_files = glob.glob(path)

# %%
ls_files.sort()

# %%
P='PATH'
N='NAME'
D='DOM'
O='OUT'
ND = 'NAME_DAY'
DO = 'DIR_OUT'
df = pd.DataFrame(ls_files,columns=[P])

# %%
df[N]=df[P].apply(lambda p: os.path.basename(p))
df[ND]=df.apply(lambda r: os.path.basename(os.path.dirname(r[P])),axis=1)
df[O]=df.apply(lambda r: os.path.join(PATH_OUT,r[ND],r[N]+'.jpg'),axis=1)
df[DO]=df.apply(lambda r: os.path.dirname(r[O]),axis=1)
df[D]=df[N].str.extract('_d0(.)').astype(int)
df

# %%

# %%
_dn = df[ND]
_dn = _dn.drop_duplicates()
_dd = df[D]
_dd = _dd.drop_duplicates()

# %%
for dom in _dd:
    for day in _dn:
        dfs = df[(df[ND]==day)&(df[D]==dom)]
        out = dfs[DO].iloc[0]+'.jpg'
        print(out)
        ax = axsplot()
        try:
            ds =xr.open_mfdataset(dfs.iloc[:][P],concat_dim=co.TIME,combine='nested', preprocess=fa.convert_ds_time_format)
            ds.sum(fa.get_dims_complement(ds,co.TIME))[co.CONC].plot(ax=ax)
        except: pass
        ax.figure.savefig(out)
        plt.close(ax.figure)
        


# %%
