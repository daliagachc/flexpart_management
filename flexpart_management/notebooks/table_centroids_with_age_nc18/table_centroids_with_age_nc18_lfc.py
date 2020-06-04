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

from useful_scit.imps import *
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

plt;
# %%
ORDER = co.get_nc18_order()[::-1]['18_NC']
ORDER6 = co.get_nc18_order()[::-1]['06_NC']
ORDER6 = ORDER6[~ORDER6.duplicated()]


class TablePlot:
    def __init__(self, df, cwidth=1, rheight=.3,
                 title_size=10, text_size = 8,
                 round_dic:dict=None):
        self.df: pd.DataFrame = df
        self.nc: int = len(df.columns) + 1
        self.nr: int = len(df)
        self.cwidth = cwidth
        self.rheight = rheight
        self.width = self.nc * self.cwidth
        self.height = self.nr * self.rheight
        self.splot = splot(1, self.nc,
                           figsize=(self.width, self.height),
                           sharey=True
                           )
        self.tit_size = title_size
        self.round_dic = round_dic
        self.text_size = text_size

    def plot_label(self):
        for i, l in enumerate(self.df.index):
            self.splot.axf[0].annotate(l, [.5, i],
                                       verticalalignment='center',
                                       horizontalalignment='center',
                                       size = self.text_size
                                       )
            self.splot.axf[0].set_title(
                self.df.index.name,
                fontdict={'fontsize': self.tit_size}
            )

    def plot_col(self, col: str, ax=plt.Axes):
        self.df[col].plot.barh(
            ax=ax, alpha=.15, color='k', width=.7
        )
        ax.set_title(col, fontdict={'fontsize': self.tit_size})

    def plot_cols(self):
        for c, ax in zip(self.df.columns, self.splot.axf[1:]):
            self.plot_col(c, ax)
            if self.round_dic is None:
                f = ' {:.1f} '
            else:
                f = f' {{:.{self.round_dic[c]}f}} '
            self.add_lab(ax, c, f =f )

    def despine(self):
        for ax in self.splot.axf:
            ax.set_xticks([])
            ax.set_yticks([], minor=True)
            ax.set_yticks([], minor=False)
            ax.tick_params(left=False)
            sns.despine(ax=ax, bottom=True, left=True)

    def add_lab(self, ax: plt.Axes, col: str, f=' {:.1f} '):
        ser = self.df[col]
        x0, x1 = ax.get_xlim()
        xlen = x1 - x0
        xmid = x0 + xlen / 2
        for i, (l, v) in enumerate(ser.items()):
            if v > xmid:
                lr = 'right'
            else:
                lr = 'left'
            ax.annotate(
                f.format(v), [v, i],
                verticalalignment='center',
                horizontalalignment=lr,
                size = self.text_size
            )


def ax_label(ax: plt.Axes, dfa: pd.DataFrame):
    for i, l in enumerate(dfa.index):
        ax.annotate(l, [.5, i + .5],
                    verticalalignment='center',
                    horizontalalignment='center',
                    )
    pass


def get_par(ds, lab, nc_='conc_lab_nc18', order=ORDER):
    age = ds[lab].loc[{'z_column': 'ALL'}]
    con = ds[nc_].loc[{'z_column': 'ALL'}]
    if 'normalized' in con.dims:
        con = con.loc[{ 'normalized': 0}]
    age_labs = (age * con).sum(co.RL) / con.sum(co.RL)
    age_labs = age_labs.load().to_dataframe(name='age')['age']
    age_labs = age_labs.loc[order]
    return age_labs





def add_lab(ax: plt.Axes, ser: pd.Series, f=' {:.1f} '):
    x0, x1 = ax.get_xlim()
    xlen = x1 - x0
    xmid = x0 + xlen / 2
    for i, (l, v) in enumerate(ser.items()):
        if v > xmid:
            lr = 'right'
        else:
            lr = 'left'
        ax.annotate(
            f.format(v), [v, i],
            verticalalignment='center',
            horizontalalignment=lr
        )


def get_tot(ds, nc_='conc_lab_nc18', order=ORDER):
    age = ds[nc_].loc[{'z_column': 'ALL', 'normalized': 0}]
    con = ds['conc_all'].loc[{'z_column': 'ALL', 'normalized': 0}]
    age_labs = (age).sum(co.RL) / con.sum(co.RL)
    age_labs = age_labs.load().to_dataframe(name='age')['age']
    age_labs = age_labs.loc[order] * 100
    return age_labs


def get_rat(ds, nc_='conc_lab_nc18', order=ORDER):
    age = ds[nc_].loc[{'z_column': 'BL', 'normalized': 0}]
    con = ds[nc_].loc[{'z_column': 'ALL', 'normalized': 0}]
    age_labs = (age).sum(co.RL) / con.sum(co.RL)
    age_labs = age_labs.load().to_dataframe(name='age')['age']
    age_labs = age_labs.loc[order] * 100
    return age_labs


# %%
def get_nc6(IND, SRR, dfa):
    _d = dfa.copy()
    _d['nc6'] = co.get_nc18_order().set_index('18_NC')['06_NC']
    g = _d.reset_index().groupby('nc6')
    _s = g[[SRR]].sum()
    _s[IND] = g[IND].last()
    s6 = \
        pd.merge(_d['nc6'].reset_index(), _s, how='left', on=IND).set_index(
            IND)[
            SRR]
    return s6

def fix_index(dfa, tp):
    ax0 = tp.splot.axf[0]
    df1 = dfa.copy()
    df1['col'] = .25
    df1['nc6'] = co.get_nc18_order().set_index('18_NC')['06_NC']
    df1['c'] = df1['nc6'].apply(lambda x: sns.desaturate(co.pw_col_dict[x], .9))
    # plt.barh()
    df1['col'].plot.barh(ax=ax0, width=1, bottom=-.5, left=-.3, color=df1['c'])
    ax0.set_yticks([])
    ax0.set_ylabel(None)
    ax0.set_xlim(-.5, 1)
    for yy in [-.5, 2.5, 5.5, 9.5, 12.5, 14.5, 17.5]:
        ax0.axhline(yy, linewidth=4, color='w', alpha=1)
    return df1

def fix_index6(dfa, tp):
    ax0 = tp.splot.axf[0]
    df1 = dfa.copy()
    df1['col'] = .25
    df1['nc6'] = df1.index
    df1['c'] = df1['nc6'].apply(lambda x: sns.desaturate(co.pw_col_dict[x], .9))
    # plt.barh()
    df1['col'].plot.barh(ax=ax0, width=1, bottom=-.5, left=-.3, color=df1['c'])
    ax0.set_yticks([])
    ax0.set_ylabel(None)
    ax0.set_xlim(-.5, 1)
    for yy in range(7):
        ax0.axhline(yy-.5, linewidth=4, color='w', alpha=1)
    return df1


def fix_main_pw(df1, tp:TablePlot):
    ax = tp.splot.axf[7]
    for artist in ax.lines + ax.collections + ax.texts:
        artist.remove()
    _df = df1['nc6'].reset_index().reset_index().groupby(
        'nc6').last().reset_index()
    for l, r in _df.iterrows():
        ax.annotate(r['nc6'], [0, r['index']],
                    verticalalignment='center',
                    horizontalalignment='center',
                    size = tp.text_size
                    )


def add_blines(tp):
    for ax in tp.splot.axf[:]:
        for yy in [-.5, 2.5, 5.5, 9.5, 12.5, 14.5, 17.5]:
            ax.axhline(yy, linewidth=.5, color='k', alpha=1)

def add_blines6(tp):
    for ax in tp.splot.axf[:]:
        for yy in [-.5,5.5]:
            ax.axhline(yy, linewidth=.5, color='k', alpha=1)



SRR = 'SRR [%]\n$n_c=18$'
IND = '    short\n    name'
DIS = 'distance\nfrom\nCHC [km]'
ZGL = 'height\nabove\nground [km]'
ZSL = 'height\nabove sea\nlevel [km]'
SRRR = r'$\frac{SRR_{<1.5\mathrm{km}}}' \
       r'{SRR_{\mathrm{tot}}}$ [%]'
AGE = 'age [h]'
MPW = 'main \npath way'
SRR6 = 'SRR [%]\n$n_c=6$'


def get_plot_df(ds):
    dfa = pd.DataFrame()
    dfa[SRR] = get_tot(ds)
    dfa.index.name = IND
    dfa[DIS] = get_par(ds, 'r_dis_lab_nc18') * 100
    dfa[ZGL] = get_par(ds, 'zgl_lab_nc18') / 1000
    dfa[ZSL] = get_par(ds, 'zsl_lab_nc18') / 1000
    dfa[SRRR] = get_rat(ds)
    dfa[AGE] = get_par(ds, 'age_lab_nc18')
    dfa[MPW] = 0
    dfa[SRR6] = get_nc6(IND, SRR, dfa)
    return dfa

def get_plot_df_6(ds):
    dfa = pd.DataFrame()
    dfa[SRR] = get_tot(ds,nc_='conc_lab_nc06',order=ORDER6)
    dfa.index.name = IND
    dfa[DIS] = get_par(ds,nc_='conc_lab_nc06', lab='r_dis_lab_nc06',order=ORDER6) * 100
    dfa[ZGL] = get_par(ds, nc_='conc_lab_nc06',lab='zgl_lab_nc06',order=ORDER6) / 1000
    dfa[ZSL] = get_par(ds, nc_='conc_lab_nc06',lab='zsl_lab_nc06',order=ORDER6) / 1000
    dfa[SRRR] = get_rat(ds,nc_='conc_lab_nc06',order=ORDER6)
    dfa[AGE] = get_par(ds, nc_='conc_lab_nc06',lab='age_lab_nc06',order=ORDER6)
    return dfa

def round_dic():
    dic = {
        SRR : 1,
        IND : 0,
        DIS : 0,
        ZGL : 1,
        ZSL : 1,
        SRRR: 0,
        AGE : 0,
        MPW : 1,
        SRR6: 1,
    }
    return dic
