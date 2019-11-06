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
# this notebook was created to convert rectanfular coo


# %%
import flexpart_management.modules.FLEXOUT as FO
# noinspection PyUnresolvedReferences
import flexpart_management.modules.flx_array as fa
from useful_scit.imps import *
# %%
handler = log.log.StreamHandler(sys.stdout)
formatter = log.log.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
log.ger.addHandler(handler)


log.ger.setLevel(log.log.DEBUG)

# %%
# doms = ['d01','d02']
# root_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/*-*-*'
# root_path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-08-18_18-46-19_/*-*-*'
# path_out = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-08-18_18-46-19_/log_pol'
def main():
    root_path = sys.argv[1]
    path_out = os.path.join(os.path.dirname(root_path),'log_pol')
    log.ger.debug(f'path out is {path_out}')

    # print('path_out', path_out)
    dom = sys.argv[2]
    # run_name = 'run_2019-10-02_13-42-52_'
    run_name = sys.argv[3]
    paths = glob.glob(root_path)
    paths.sort()

    # %%
    fo_base_dic = dict(
        # dom = 'd01',
        # folder_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10',
        folder_path_out=path_out,
        run_name=run_name,
    )

    # %%
    for p in paths:
        log.ger.debug(f'path is {p}')
        log.ger.debug(f'dom  is {dom}')
        # print('starting', dom, p)
        new_dic = dict(dom=dom, folder_path=p)
        fo_dic = {**fo_base_dic, **new_dic}

        # noinspection PyBroadException
        try:
            fo = FO.FLEXOUT(**fo_dic)
            fo.export_log_polar_coords(keep_z=True)
            log.ger.debug(f'done {p} {dom}')
        except:
            log.ger.error(f'fail {p} {dom}')
# %%
main()
