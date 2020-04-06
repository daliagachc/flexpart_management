# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import flexpart_management.notebooks.six_clusters_centroids.\
    six_clusters_centroids_lfc as lfc
from flexpart_management.notebooks.six_clusters_centroids.\
    six_clusters_centroids_lfc import *

def main():
    # %%
    def _plot_zmid(path):
        ds = open_ds(path)
        ds[co.CONC].sum([co.RL, co.TH_CENTER]).plot()
        plt.show()

    def open_ds(path):
        ds = xr.open_dataset(pjoin(co.tmp_data_path, path))
        return ds

    # %%


    _plot_zmid('ds_clustered_18.nc')
    _plot_zmid('ds_clustered_18_conc_smooth.nc')


    # %%
    ds = open_ds('ds_clustered_18.nc')
    # %%
    short_dic = {
        co.ZM       : slice(None, None, 1),
        co.TH_CENTER: slice(None, None, 1),
        co.R_CENTER : slice(None, None, 1),
        co.RL       : slice(None, None, 1)
    }
    dss = ds[short_dic].copy()
    # %%
    ds1 = fa.from_asl_to_agl(dss)

    # %%
    df = pd.read_csv(pjoin(co.tmp_data_path,'prop_df_.csv'))
    n6 = pd.read_csv(pjoin(co.tmp_data_path,'nc_18_nc_06.csv'))
    _dic = df.set_index('cluster_i')['short_name'].to_dict()
    _dic6 = n6.set_index('18_NC')['06_NC'].to_dict()

    def _fdic(i):
        # global ii
        # ii = i
        # print(i)
        if np.isnan(i):
            res = np.nan
        else:
            res = _dic[i]
        return res

    def _fdic6(i):
        # global ii
        # ii = i
        # print(i)
        if i == 'nan':
            res = np.nan
        else:
            res = _dic6[i]
        return res

    ds1['lab_name']=xr.apply_ufunc(_fdic,ds1['lab'],vectorize=True)
    ds1['lab_nc06']=xr.apply_ufunc(_fdic6,ds1['lab_name'],vectorize=True)
    # %%
    ds1=ds1.set_coords(names=['lab','lab_name','lab_nc06'])
    # %%
    fa.compressed_netcdf_save(ds1,pjoin(co.tmp_data_path,'ds_clustered_18_agl.nc'))
    # %%





    # %%

    # %%
    ds1

    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%




# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%


