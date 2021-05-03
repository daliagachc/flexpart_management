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
from flexpart_management.notebooks.bams_fig.bams_fig_lfc import *

import flexpart_management.notebooks.bams_fig.bams_fig_lfc as lfc

CONC_ALL = 'conc_all'
# %%
d1 = '2018-05-09 00'

d2 = '2018-05-24 00'

csv_file = 'diurnal_BOT_2018-05-24_2018-05-08.csv'
DIRNAME = os.path.dirname(lfc.__file__)

open_plot_save(CONC_ALL, csv_file, d1, d2, DIRNAME)

# %%
d1 = '2017-05-24 00'

d2 = '2019-05-09 00'

csv_file = 'diurnal_BOT_ALL.csv'
DIRNAME = os.path.dirname(lfc.__file__)

open_plot_save(CONC_ALL, csv_file, d1, d2, DIRNAME)
# %%
# %%
# %%
