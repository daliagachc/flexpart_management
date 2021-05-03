from useful_scit.imps2.defs import *


p = './data/cluster_series_v3.nc'


po = './data/csv'


os.makedirs(po,exist_ok=True)


ds = xr.open_dataset(p)


va = list(ds.data_vars)


for v in va:
    res = ds[v].to_dataframe()
    oo = pjoin(po,f'{v}.csv')
    res.to_csv(oo)



