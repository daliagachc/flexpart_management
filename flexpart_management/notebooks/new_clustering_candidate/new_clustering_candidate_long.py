# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from flexpart_management.notebooks.new_clustering_candidate.new_clustering_candidate_lfc import *
import flexpart_management.notebooks.new_clustering_candidate.new_clustering_candidate_lfc as lfc



# %%

def main():
    # %%
    log.ger.setLevel(log.log.DEBUG)
    # %%
    nb_dir = os.path.dirname(lfc.__file__)

    # %%
    log.ger.debug('load data')
    TAB_NAME = 'ss_data_long'
    das = load_data()

    # %%
    log.ger.debug('preprocess')
    das3 = preprocess(das)

    # %%
    sql_path = 'sqlite:///'+pjoin(nb_dir,TAB_NAME+'.db')
    # %%

    engine = create_engine(sql_path, echo=False)
    # %%

    create_res_db(engine, TAB_NAME=TAB_NAME, min_cl=25,max_cl=50,int_cl=5,rnds_len=2)

    # %%
    while True:
        r = get_next_row(engine,TAB_NAME)
        log.ger.debug('doing r %s',r)
        if r is False:
            break

        ss = get_silhouette(das3, r)
        try: update_ss(engine, r, ss, TAB_NAME)
        except:
            try: update_ss(engine, r, ss, TAB_NAME)
            except: pass

    # %%
    # %%
    log.ger.debug('nothin else to do :)')


# %%



if __name__ == '__main__':
    main()


