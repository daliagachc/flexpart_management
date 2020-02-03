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
import pandas
import seaborn
from flexpart_management.modules import constants as co
from flexpart_management.modules import flx_array as fa
from matplotlib import pyplot
from useful_scit.imps import *

# %%
from useful_scit.imps import pjoin
# %%
c45 = 'C4_C5_compounds'
c68 = 'C6_C8_compounds'
c91 = 'C9_C13_compounds'
bc  =  'BC'

r1 = 'c6_8/c4_5'
r2 = 'c9_13/c4_5'
r3 = 'BC/c4_5'
r4 = 'c4_5'


def import_time_series():
    data_path = pjoin(co.tmp_data_path, 'data_george_cc.xlsx')
    df_ft = pd.read_excel(data_path)
    df_ts = pd.read_excel(data_path, sheet_name=1, skiprows=1)
    # %%
    df_ts = df_ts.set_index(pd.to_datetime(df_ts['time_utc']))
    df_ts = df_ts.drop('time_utc', axis=1)
    return df_ft, df_ts


def plot_cols(cols, df_ts, xscale, yscale):
    for c in cols:
        data:pd.Series = df_ts[c].dropna()
        f, ax = plt.subplots()
        if xscale is 'log':
            max = data.quantile(.99)
            min = .00001 * max
            min = np.max([data.quantile(.01),min])
            bins = np.geomspace(min,max,20)
            x0 = bins[0]
            bins = [0,*bins[1:]]

            sns.distplot(data, ax=ax, bins=bins, kde=False)
            ax.set_xlim(x0,max)
        else:
            sns.distplot(data,ax=ax,kde=False)
        ax.set_yscale(yscale)
        ax.set_xscale(xscale)
        plt.show()

class Data:
    name:str = None
    candidate_ft_ts = None
    excel_ts = None
    ds:xr.Dataset = None
    c_cols = [c45,c68,c91,bc]
    r_cols = [r1,r2,r3,r4]
    r_pcols = ['p-'+r for r in r_cols]
    ds_jan:xr.Dataset = None
    ds_flx:xr.Dataset = None
    '''flexpart dataset'''

    def __init__(self):
        pass

    def import_time_seres(self):
        self.candidate_ft_ts, self.excel_ts = import_time_series()
        self.ds_flx = fa.open_temp_ds('ds_clustered_18.nc')

    def jan_ds_slice(self):
        self.ds_jan = self.ds[{'time_utc':self.ds['jan']}]


    def create_ds(self):
        ds = self.excel_ts.to_xarray()
        ds = ds.drop(['month', 'day', 'Hour'])
        # %%
        ds = ds.set_coords('Time_LT')
        # %%
        ds = ds.assign_coords(month=ds['time_utc'].dt.month)
        ds = ds.assign_coords(hour=ds['time_utc'].dt.hour)
        is_jan = ds['time_utc'].dt.month == 1
        ds = ds.assign_coords(jan=is_jan)

        self.ds=ds

    def add_ratios(self,ds_s='ds'):

        ds = getattr(self,ds_s)
        ds[r1] = ds[c68]/ds[c45]
        ds[r2] = ds[c91]/ds[c45]
        ds[r3] = ds[bc]/ds[c45]
        ds[r4] = ds[c45]

        setattr(self,ds_s,ds)

    def add_quantiles(self, ds_s='ds'):
        from sklearn.preprocessing import QuantileTransformer as QT
        from sklearn_xarray import wrap

        ds:xr.Dataset = getattr(self, ds_s)
        if 'dummy' not in list(ds.dims):
            ds = ds.expand_dims('dummy')


        for r, qr in zip(self.r_cols, self.r_pcols):
            _is_inf = ds[r] == np.inf
            no_inf_max = ds[r].where(~_is_inf).max()
            da = ds[r].copy()
            da = da.where(~_is_inf,no_inf_max)
            qt = wrap(QT,sample_dim='time_utc')
            ds[qr] = qt.fit_transform(da.transpose('time_utc','dummy'))

        setattr(self,ds_s,ds)

    def cluster_ds(self, ds_s='ds',num_of_c = 2):
        ds:xr.Dataset = getattr(self,ds_s)
        from sklearn.cluster import KMeans
        from sklearn_xarray import wrap
        da = ds[self.r_pcols].to_array(dim='cluster_vars',name='quan_value')
        log.ger.debug(da.max())
        # return da
        da = da.dropna(dim = 'time_utc',how='any')

        # return da

        if 'dummy' in list(da.dims):
            da = da[{'dummy':0}]
        km = wrap(KMeans(n_clusters=num_of_c),sample_dim='time_utc')
        fit = km.fit(da)

        labs = xr.DataArray(fit.labels_,
                            coords={'time_utc':da['time_utc']},
                            dims=['time_utc'])
        da = da.assign_coords({'labs':labs})
        return fit,da


