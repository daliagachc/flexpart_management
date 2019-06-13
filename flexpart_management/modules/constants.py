# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import cartopy
import numpy as np

PROJ = cartopy.crs.PlateCarree()
TIME = 'Time'
AC = 'ageclass'
TH = 'Time_h'
WE = 'west_east'
SN = 'south_north'
TOPO = 'TOPOGRAPHY'
ZM = 'ZMID'
ZB = 'ZBOT'
ZT = 'ZTOP'
ZLM = 'ZLEN_M'
ALT = 'ALT'
BT = 'bottom_top'
RL = 'releases'
VOL = 'VOL'
GA = 'GRIDAREA'
CONC = 'CONC'
LAT = 'LAT'
LON = 'LON'
LL_DIS = 'LL_DIS'
LL_ANG = 'LL_ANG'
ACTUAL_TIME = 'ACTUAL_TIME'
R_CENTER = 'R_CENTER'
TH_CENTER = 'TH_CENTER'
LAT_00 = 'LAT_00'
LAT_10 = 'LAT_10'
LAT_11 = 'LAT_11'
LAT_01 = 'LAT_01'
LON_00 = 'LON_00'
LON_10 = 'LON_10'
LON_11 = 'LON_11'
LON_01 = 'LON_01'
CHC_LAT = -16.350427
CHC_LON = -68.131335
LPB_LAT = -16.507125
LPB_LON = -68.129299

LL00 = [LAT_00,
        LAT_10,
        LAT_11,
        LAT_01,
        LON_00,
        LON_10,
        LON_11,
        LON_01, ]

ROUND_R_LOG = .18
ROUND_TH_RAD = np.pi/18

CPer = 'CONC_per'
CC = 'CONC_conc'
CCPer = 'CONC_conc_per'
ClusFlag = 'flags'

COL = 'CON_TIME/LEN'

LALO_LAPAZ = [-70, -66, -18, -14]
LALO_BOL = [-83, -43, -35, 2]


print('reload')

FLAGS = 'flags'
H = 'H'

PLOT_LABS = {
        CPer: 'mass*res. time[%]',
        H:'height [masl]',
        ZM: 'height [mag]',
        CONC: 'mass/mass * res. time [s]'
}







