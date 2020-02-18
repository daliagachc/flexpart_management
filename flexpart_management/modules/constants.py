# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import cartopy
import numpy as np
import os

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
ROUND_TH_RAD = np.pi / 18

CPer = 'CONC_per'
CC = 'CONC_conc'
CCPer = 'CONC_conc_per'
ClusFlag = 'flags'
LAB = 'lab'

COL = 'CON_TIME/LEN'

LOLA_LAPAZ = [ -70, -66, -18, -14 ]
LOLA_BOL = [ -83, -43, -35, 2 ]

print('reload')

FLAGS = 'flags'
H = 'H'

PLOT_LABS = {
    CPer: 'mass*res. time[%]',
    H   : 'height [masl]',
    ZM  : 'height [mag]',
    CONC: 'mass/mass * res. time [s]',
    CC  : 'mass/(mass * res. time * vol) [s/m3]',
}

CLUS_LENGTH_DIM = 'CLUS_LENGTH_DIM'
CONC_NORMALIZED = 'CONC_NORMALIZED'
CONC_NORMS = 'CONC_NORMS'
DUM_STACK = 'dum'
FLAG = 'FLAG'
KMEAN_OBJ = 'KMEAN_LAB'
LAB_CLUSTER_THRESHOLD = 'LAB_CLUSTER_THRESHOLD'
SIL_SC = "SIL_SCORE"
SIL_SAMPLE = "SIL_SAMPLE"
DIS = 'Distance CHC [km]'
AGECLASS = 'ageclass'
SPECIES = 'species'
RECEPTORS = 'receptors'

XLONG_CORNER = 'XLONG_CORNER'
XLAT_CORNER = 'XLAT_CORNER'
ZTOP = 'ZTOP'
# AGECLASS = 'ageclass'
RELEASENAME = 'ReleaseName'
RELEASETSTART_END = 'ReleaseTstart_end'
RELEASEXSTART_END = 'ReleaseXstart_end'
RELEASEYSTART_END = 'ReleaseYstart_end'
RELEASEZSTART_END = 'ReleaseZstart_end'
RELEASENP = 'ReleaseNP'
TOPOGRAPHY = 'TOPOGRAPHY'
GRIDAREA = 'GRIDAREA'
RELEASE_TIME = 'RELEASE_TIME'
WEST_EAST = 'west_east'
SOUTH_NORTH = 'south_north'
XLONG = 'XLONG'
XLAT = 'XLAT'

VLONG = 'VLONG'
VLAT = 'VLAT'

D1 = 'd01'

D2 = 'd02'


HEAD_VARS = [
    XLONG_CORNER,
    XLAT_CORNER,
    ZTOP,
    AGECLASS,
    RELEASENAME,
    RELEASETSTART_END,
    RELEASEXSTART_END,
    RELEASEYSTART_END,
    RELEASEZSTART_END,
    RELEASENP,
    TOPOGRAPHY,
    GRIDAREA,
]

CSUM = 'CONC_SUM'

RAD_MIN = 00.07
"""minimum radial distance to consider in the algorithm"""
RAD_MAX = 20.00
"""maximum radial distance to consider in the algorithm """

above_thre_label = 'above_thre'
CONC_SMOOTH_NORM = 'conc_smooth_norm'
short_range_clusters = [13,17,3,2,11,16]
short_range_clusters.sort()
mid_short_range_clusters = [5,10,6,12]
mid_short_range_clusters.sort()
mid_range_clusters = [15,1,14,7,8]
mid_range_clusters.sort()
long_range_clusters = [9,0,4]
long_range_clusters.sort()
tmp_data_path = '/Users/diego/flexpart_management/flexpart_management/tmp_data'
latest_ds_mac = os.path.join(tmp_data_path,'ds_clustered_18_conc_smooth.nc')
prop_df_path = os.path.join(tmp_data_path, 'prop_df_.csv')

silhouette_path = os.path.join(tmp_data_path,'silhouette_scores.pickle')
# %%

import flexpart_management
fm_path = flexpart_management.__file__
fm_path = os.path.dirname(fm_path)

# %%
paper_fig_path = '/Users/diego/wrf-flexpart-chc/src/figures'


# %%