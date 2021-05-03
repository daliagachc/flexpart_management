# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

# %%

import flexpart_management.notebooks.itcz_analysis.itcz_analysis_lfc as lfc
from flexpart_management.notebooks.itcz_analysis.itcz_analysis_lfc import  *

# %%
ds = xr.open_dataset(pjoin(co.tmp_data_path,'pres_itcz.nc'))

# %%
import cartopy.crs as ccrs
tp_ = ds['tp']
tp_ = tp_.loc[{'time':slice('2017-12','2018-06')}]
p = tp_.plot(col='time',
             col_wrap=3,
             subplot_kws={"projection":ccrs.PlateCarree()},
             vmax = .03,
             size=2,
             aspect = 2
             # subplot_kws=dict(projection=ccrs.Orthographic(-80, 35),
             #                  facecolor="gray"),


             )
for ax in p.axes.flat:
    ax:crt.mpl.geoaxes.GeoAxesSubplot
    ax.set_extent([-120, -20,20 , -20], crs=ccrs.PlateCarree())
    ax.coastlines()
    ax.gridlines()
    ax.axhline(0, color='r')
    ax.scatter(co.CHC_LON,co.CHC_LAT,color='r')

    pass
plt.tight_layout()
plt.show()
# %%

# %%
# %%

ds = xr.open_dataset(pjoin(co.tmp_data_path,'wind_itcz.nc'))
# %%
cc,rr = 3,3
s = splot(cc,rr,subplot_kw={"projection":ccrs.PlateCarree()},
          figsize=(cc*5,rr*4.5),dpi=300,constrained_layout=True)
mm = [0,1,2,3,4,5,6]
for i in range(len(mm)):
    ax = s.axf[i]
    fa.get_ax_bolivia(ax=ax,lola_extent=[-100,-20,-40,20],
                      map_line_alpha=.1,
                      grid_alpha=0,
                      plot_cities=False,
                      draw_labels=False,
                      chc_lp_legend=False)
    da:xr.DataArray = ds[{'level': 3, 'time': 11 + mm[i]}]
    coar = 15
    da = da.coarsen(**{'latitude': coar, 'longitude':coar}, boundary='trim').mean()

    u = da['u']
    v = da['v']
    la = da['latitude']
    lo = da['longitude']

    Q = ax.quiver(lo,la,u,v,scale=100)
    qk = ax.quiverkey(Q, .9, 1.05, 10, r'$10 \frac{m}{s}$', labelpos='E',
                       coordinates='axes')
    ax.set_title(f'pres: {da["level"].item()} | date: {da["time"].dt.strftime("%Y-%m").item()}')
    # ax.coastlines()
plt.show()

# %%


axf = s.axf


for i in range(7):
    da = ds[{'level':-1,'time':11+i}]
    u = da['u']
    v = da['v']
    ax = axf[i]

    x, y = np.meshgrid(u['longitude'].values, u['latitude'].values)
    ax: crt.mpl.geoaxes.GeoAxesSubplot
    ax.set_extent([-120, -20, 20, -20], crs=ccrs.PlateCarree())
    ax.barbs(x,y,u=u.values,v=v.values,
             length=4, regrid_shape=(20,10),
             )
    ax.coastlines()
    # ax.gridlines()
    ax.axhline(0, color='r')
    ax.scatter(co.CHC_LON, co.CHC_LAT, color='r')
    # plt.show()
plt.show()

