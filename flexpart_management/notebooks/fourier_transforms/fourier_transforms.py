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

import flexpart_management.notebooks.fourier_transforms. \
    fourier_transforms_lfc as lfc
from flexpart_management.notebooks.fourier_transforms. \
    fourier_transforms_lfc import *


# %%
def main():
    # %%
    ds = lfc.open_ds()
    # ls18 = list(ds[lfc.C18]['lab_nc18'].values)
    ls18 = co.get_nc18_order().sort_values(['sr', '18_NC'])['18_NC'].values
    # %%
    col_df = lfc.get_fourier_for_all_df(ds, ls18)
    col_df.index = 1/col_df.index
    mean_ds = col_df.median(axis=1)

    # %%

    s = lfc.plot_fourier_list(col_df, ls18, mean_ds)
    s.f.savefig(pjoin(lfc.img_path, 'c18_fourier.pdf'))
    # %%
    # %%
    import scipy as sp
    lab = '07_LR'
    temp = get_df(lab, ds)
    temp_fft = sp.fftpack.fft(temp.values)
    temp_psd = np.abs(temp_fft) ** 2
    fftfreq = sp.fftpack.fftfreq(len(temp_psd), 1. / 24)
    i = fftfreq > 0
    temp_fft_bis = temp_fft.copy()
    absf = np.abs(fftfreq)
    # _b2 = np.abs(fftfreq) >= 1.1

    # temp_fft_bis[absf>1.1] = 0
    temp_fft_bis[absf < .9] = 0
    temp_slow = np.real(sp.fftpack.ifft(temp_fft_bis))
    new_df = pd.Series(temp_slow, index=temp.index)

    new_df.plot()
    plt.show()
    # %%
    s = lfc.plot_daily_evolution(ds, ls18)
    s.f.show()
    s.f.savefig(pjoin(img_path, 'daily_evolution_nc18.pdf'))
    # %%
    ds
    # %%

    # %%
    # cl_lab = '09_MR'
    sel = [
        ['02_SR', [1,0]],
        # '04_SR',
        ['07_SR', [1,0]],
        ['10_SR', [0,1]],
        # '11_SR',
        ['12_SR', [0,1]]
    ]
    for cl_lab, _in in sel:
        # %%
        h0, h1 = 0, 24
        nc = 2
        dds, km = lfc.get_dds_km(cl_lab, ds, z='ALL', h0=h0, h1=h1, nc=nc)
        # %%
        s = lfc.plot_ts_clus(dds, km, cl_lab, h0=h0, h1=h1, _in=_in)
        # %%
        name = f'day_dtw_kmean_{cl_lab}.pdf'
        # s.f.savefig(pjoin(img_path, name))
        s.f.savefig(pjoin(co.paper_fig_path, name))
        # break
    # for cl_lab in sel:
    #     h0, h1 = -12, 12
    #     dds, km = lfc.get_dds_km(cl_lab, ds, z='ALL', h0=h0, h1=h1, nc=nc)
    #     s = lfc.plot_ts_clus(dds, km, cl_lab, h0=h0, h1=h1)
    #     name = f'night_dtw_kmean_{cl_lab}.pdf'
    #     s.f.savefig(pjoin(img_path, name))
    #     # break

    # %%

    pass

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
