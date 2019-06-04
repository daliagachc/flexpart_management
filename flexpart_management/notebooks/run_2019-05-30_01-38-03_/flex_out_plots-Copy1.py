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
# %load_ext autoreload
# %autoreload 2

# %%
import flexpart_management.modules.flx_array as fa

# %%
ds = xr.open_dataset('/tmp/dd4.nc')
ds2 = xr.open_dataset('/tmp/dd02.nc')

# %%

# %%
la = ds.LAT - fa.CHC_LAT
lo = ds.LON - fa.CHC_LON
r = np.sqrt(la**2+lo**2)

# %%
r.max()

# %%
r1=.05
r2=30
n=20
rlog_space = np.linspace(np.log(r1),np.log(r2),n)
r_space = np.e**rlog_space

# %%
plt.figure()
plt.plot(rlog_space)
plt.figure()
plt.plot(r_space)

# %%
RS = 'r_space'
RD = 'r_dis'
RC = 'r_center'
df_r = pd.DataFrame(r_space,columns=[RS])
df_r[RD] = df_r[RS] - df_r[RS].shift()
df_r = df_r*100
df_r[RC] = (df_r[RS] + df_r[RS].shift())/2


# %%
df_r

# %%

# %%
plt.plot(ints)

# %%
ints*100


# %%

# %%
