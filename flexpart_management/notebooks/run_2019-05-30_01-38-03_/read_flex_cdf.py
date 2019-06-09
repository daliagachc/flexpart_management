# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import *

# %%
import flexpart_management.modules.constants

path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10'
dom = 'd01'
header = 'header_'
flx = 'flxout'

# %%
# %load_ext autoreload
# %autoreload 2

# %%
import flexpart_management.modules.flx_array as fa

# %%
head_ds = fa.import_head_ds(path,dom)

# %%
file_ds_list = fa.import_file_ds_list(path,dom)

# %%
ds_con = fa.concat_file_ds_list(file_ds_list)

# %%
ds_con1 = fa.convert_ds_time_format(ds_con)

# %%
ds_join = fa.join_head(ds_con1,head_ds)

# %%
ds1 = fa.add_release_time_dim(ds_join,head_ds)

# %%
ds2 = fa.assign_vars_to_cords(ds1)
ds2 = fa.add_lat_lot(ds2)
ds2 = fa.add_zmid(ds2)
ds2 = fa.add_zbot(ds2)
ds2 = fa.add_zlength_m(ds2)


# %%
ds2

# %%
ds2_1 = ds2.copy()
ds2_1['CONC']=1/ds2_1.CONC.where(ds2_1.CONC>0.0000)

# %%
dsV = ds2.GRIDAREA*ds2.ZLEN_M

# %%
dsC = ds2.CONC.isel(Time=-5)
dsC = dsC.where(dsC>0.000)

# %%
dcC_1 = (1/dsC)

# %%
(dcC_1/dsV).sum()

# %%
(dcC_1*dsV).sum()/3600/3600

# %%
dsS = dsC / dsV
dsS_1 = 1/dsS

# %%
V_res = (68.14-68.118)* 100000 * \
(16.355-16.335)*100000 * \
300*1000e-14

# %%
V_res

# %%
(dsC).sum()/3600

# %%
ds2.CONC.sum(dim=['bottom_top','south_north','west_east']).plot()

# %%
ds2_1.CONC.sum(dim=['bottom_top','south_north','west_east']).plot()

# %%

# %%

# %%

# %%

# %%
head_ds.XLONG.isel(south_north=1)

# %%

# %%
cmap = mpl.colors.ListedColormap(sns.color_palette('Reds',20))

# %%
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt


fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent([-80, -50, -30, 0], crs=ccrs.PlateCarree())

# ax.add_feature(cfeature.LAND)
# ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
# ax.add_feature(cfeature.LAKES, alpha=0.5)
# ax.add_feature(cfeature.RIVERS)




# %%
ds2.CONC.mean(dim=['Time','bottom_top']).plot(vmax=.1,x='XLONG',y='XLAT',cmap=cmap,figsize=(10,10))

# %%
ds2.CONC.mean(dim=['Time','south_north']).plot(x='lon',y='ZMID',vmax=.1,figsize=(10,10))

# %%
ds2.TOPOGRAPHY.plot(x='lon',y='lat')

# %%
ds2

# %%
qa = xla.quantile([.2,.5,.8],'west_east')

# %%
(qa.isel(quantile=0)-qa.isel(quantile=-1)).plot()

# %%
ds2.CONC.isel(Time=-5).mean(dim='bottom_top').plot(vmax=.1,figsize=(10,10))

# %%
ds2.CONC.isel(Time=-5).mean(dim='south_north').plot(vmax=0.1)

# %%
ds2.CONC.isel(Time=-3).mean(dim='west_east').plot(vmax=0.1,x='south_north',y='ZTOP')

# %%
fa.add_lat_lot(ds2)

# %%
ds2.GRIDAREA.plot()

# %%
res = ds2.lat - ds2.lat.shift(south_north=1)
res.plot()

# %%
res = ds2.lon - ds2.lon.shift(west_east=1)
res.plot()

# %%
ds2.lat.min()
ds2.lat.max()

# %%
.099*100

# %%
ds2.CONC

# %%
ds2

# %%
path = '/Volumes/mbProD/Downloads/flexpart/runs/run_2019-05-31_16-01-17_1_1'

# %%
file = '/Volumes/mbProD/Downloads/flexpart/runs/run_2019-05-31_16-01-17_1_1/flxout_d02_20171209_170000.nc'
ds11 = xr.open_dataset(file)

# %%
file = '/Volumes/mbProD/Downloads/flexpart/runs/run_2019-05-31_16-01-17_2_1/flxout_d02_20171209_170000.nc'
ds21 = xr.open_dataset(file)

file = '/Volumes/mbProD/Downloads/flexpart/runs/run_2019-05-31_16-01-17_2_2/flxout_d02_20171209_170000.nc'
ds22 = xr.open_dataset(file)

file = '/Volumes/mbProD/Downloads/flexpart/runs/run_2019-05-31_16-01-17_1_2/flxout_d02_20171209_170000.nc'
ds12 = xr.open_dataset(file)

# %%
(ds21.CONC/ds11.CONC).isel(releases=1).plot()

# %%
(ds22.CONC/ds11.CONC).isel(releases=1).plot()

# %%
(ds21.CONC/ds22.CONC).isel(releases=1).plot()

# %%
(ds21.CONC/ds12.CONC).isel(releases=1).plot()

# %%
(ds11.CONC/ds12.CONC).isel(releases=1).plot()

# %%
(ds22.CONC/ds12.CONC).isel(releases=1).plot()

# %%
(ds11.CONC/ds22.CONC).isel(releases=1).plot()

# %%
ds11.CONC.isel(releases=0).sum()

# %%
ds22.CONC.isel(releases=0).sum()

# %%
ds12.CONC.isel(releases=0).sum()

# %%
ds21.CONC.isel(releases=0).sum()

# %%
ds22.CONC.isel(releases=0).sum(dim=['bottom_top']).plot()

# %%
ds22.CONC.isel(releases=0).sum(dim=['south_north']).plot(x='west_east')

# %%
hp = '/Volumes/mbProD/Downloads/flexpart/runs/run_2019-05-31_16-01-17_1_1/header_d01.nc'

# %%
xr.open_dataset(hp).TOPOGRAPHY.plot(x='XLONG',y='XLAT')

# %%
hp = '/Volumes/mbProD/Downloads/flexpart/runs/run_2019-05-31_16-01-17_1_1/header_d02.nc'
xr.open_dataset(hp).TOPOGRAPHY.plot(x='XLONG',y='XLAT')

# %%
path = '/Volumes/mbProD/Downloads/flexpart/runs/run_2019-05-31_16-01-17_2_2/'
dom = 'd02'

# %%
head_ds = fa.import_head_ds(path,dom)

# %%
file_ds_list = fa.import_file_ds_list(path,dom)

# %%
ds_con = fa.concat_file_ds_list(file_ds_list)

# %%
ds_con1 = fa.convert_ds_time_format(ds_con)

# %%
ds_join = fa.join_head(ds_con1,head_ds,ageclass=0,releases=slice(0,None))

# %%
ds2 = ds_join
# ds2 = fa.add_release_time_dim(ds2,head_ds)
ds2 = fa.assign_vars_to_cords(ds2)
ds2 = fa.add_lat_lot(ds2)
ds2 = fa.add_zmid(ds2)
ds2 = fa.add_zbot(ds2)
ds2 = fa.add_zlength_m(ds2)
ds2 = fa.add_alt_m(ds2)
ds2 = fa.add_volume(ds2)


# %%
ds2.isel(releases=0).sum(dim=['south_north','bottom_top','west_east']).CONC.plot()

# %%
ds_ = ds2.isel(releases=0)
(ds_.CONC/ds_.VOL).sum(dim=['south_north','bottom_top','west_east']).plot()

# %%
ds2.isel(releases=1).sum(dim=['bottom_top','Time']).CONC.plot(x='lon',y='lat',vmax=90,figsize=(10,10))

# %%
ds2.isel(releases=1).sum(dim=['west_east','Time']).CONC.plot(x='lat',y='ZMID',vmax=500)

# %%
ds2.isel(releases=0).sum(dim=['west_east','Time']).CONC.plot(x='lat',y='ZMID',vmax=500)

# %%
ds2['alt']=ds2.ALT

# %%
import wrf


# %%
ds22=ds2.copy()
dc = ds22.coords
ds22 = ds2.drop(dc).isel(Time=[-20,-1],releases=1)
ds22['con/vol'] = (ds22.CONC/ds2.VOL)
co = ds22.coords
ds22 = ds22.drop(co)

# %%
ds22['alt']=ds22.alt.transpose('bottom_top','south_north','west_east')

# %%
nds = wrf.interplevel(ds22['con/vol'],ds22.alt,desiredlev=np.arange(0,20000,100))

# %%
nds.mean(dim=['west_east','Time']).plot(vmax = 1e-11,figsize=(10,10))

# %%
la, lo = -16.355000,-68.140000
dis = np.sqrt((la-ds2.lat)**2+(lo-ds2.lon)**2)
mi =dis.min()

# %%
min_loc = dis.where(dis==mi).dropna(flexpart_management.modules.constants.SN, 'all').dropna(
    flexpart_management.modules.constants.WE, 'all')

# %%
dsll = ds2[flexpart_management.modules.constants.TOPO].swap_dims({flexpart_management.modules.constants.WE: 'lon',
                                                                  flexpart_management.modules.constants.SN: 'lat'})

# %%
dsll.interp(lat=la,lon=lo)

# %%
import flexpart_management.modules.create_release_file as rf

# %%
dtm = dt.datetime(2017,1,1,1,1,1)

# %%
rf.format_dt_to_str(dtm)

# %%
dc = dict(start_dt_rel=dtm, end_dt_rel=dtm)

# %%
df =rf.create_dic_range(
    d_start = dt.datetime(2018,1,1,1,0,0),
    d_end   = dt.datetime(2018,1,1,10,0,0),
    base_dict = {}

)

st= df[rf.RELEASE_DIC_STR_KEY]


# %%
st.iloc[0]

# %%
join(['s','b'])

# %%
str_out = ''
for s in st.values:
    str_out = str_out+'\n'+s
str_out = str_out[1:]

# %%
str_out

# %%
print(df.release_dic_formatted.to_string())

# %%
type(df.iloc[0].start_dt_rel) == (dt.datetime or pd.Timestamp )

# %%
type(df.iloc[0][rf.START_DT_REL_KEY])

# %%
ss = df.start_dt_rel

# %%
ss.dt.strftime('%Y%m%d_%H')

# %%
pd.Series.dt.strptime

# %%
df = rf.create_avail_file(d1='2018-01-01',d2='2018-01-10',dom00='01',frq_file=60, frq_sim=15)

# %%
rf.create_all_avail_files(d1='2018-01-01',d2='2018-01-10',frq_file=60, frq_sim=15)

# %%
df.floor('60min')[:8]

# %%
df[:4]

# %%
import flexpart_management.modules.daily_back.config_file as cf

# %%
cf.config_dic

# %%
import flexpart_management.modules.daily_back.daily_back as db

# %%
cd1 = db.generate_run_path(cf.config_dic)
cd1 = db.generate_day_path(cd1)
cd1

# %%
import flexpart_management.modules.daily_back.ConfigDayRun as CDR

# %%
cdr = CDR.ConfigDayRun()

# %%
import flexpart_management.modules.daily_back.config_file as DR

# %%
dr = DR.DayRun()

# %%
dr.generate_run_path()
dr.generate_day_path()
dr.get_dt_end_simulation()
dr.get_dt_start_simulation()
dr.get_dt_first_release()
dr.get_dt_last_release()
dr.get_release_str()
dr.create_day_path_dir()
dr.create_available_files()
dr.create_available_paths()
dr.get_input_templ_string()
dr.fill_out_templ_string()
dr.create_flx_input_path()
dr.create_flx_input_file()

# %%
dr.FLX_INPUT_PATH

# %%
os.path.join('/ts','')

# %%
