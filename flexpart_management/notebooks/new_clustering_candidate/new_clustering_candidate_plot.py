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
import \
    flexpart_management.notebooks.new_clustering_candidate.new_clustering_candidate_lfc as lfc


# %%

def main():
    # %%
    log.ger.setLevel(log.log.DEBUG)
    # %%
    nb_dir = os.path.dirname(lfc.__file__)

    # %%
    # %%


    lfc.plot_score(nb_dir,score_par='inertia')
    lfc.plot_score(nb_dir,score_par='ch_index')
    lfc.plot_score(nb_dir,score_par='db_index')
    lfc.plot_score(nb_dir,score_par='n_ss')




# %%


if __name__ == '__main__':
    main()
