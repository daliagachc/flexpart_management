# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
# %%
from useful_scit.imps import *
import flexpart_management.modules.constants as co
import sys
# %%

ts_name = 'Timeseries_for_averaging.csv'
ts_path = os.path.join(co.fm_path,
                       'requests/george/'+ts_name)
df = pd.read_csv(ts_path)


# %%
tlt = 'Time_LocalTime'
local_time = 'local_time'
utc_time = 'utc_time'
lt = pd.to_datetime(df[tlt],format='%d/%m/%Y %H:%M')
df[local_time] = lt
df[utc_time] = lt + pd.Timedelta(hours=4)
df

