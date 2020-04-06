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


# %%
import flexpart_management.notebooks.new_clustering_candidate.new_clustering_candidate_lfc\
    as lfc

# %%

nb_dir = lfc.os.path.dirname(lfc.__file__)

if __name__ == '__main__':
    lfc.script_find_ss(
        nb_dir = nb_dir,
        min_cl=1000,
        max_cl=8000,
        int_cl=1000,
        rnds_len=2,
        tab_name='ss_data_llll'
    )


