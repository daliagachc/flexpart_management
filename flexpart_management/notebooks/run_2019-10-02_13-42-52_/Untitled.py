# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import multiprocessing

# %%
multiprocessing.cpu_count()

# %%
# !echo $TMPDIR

# %%
import os

# %%
import subprocess
ls_output=subprocess.Popen(["echos 1"],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)


# %%
ls_output.returncode

# %%
ls_output.errors

# %%
ls_output.stderr

# %%
ls_output.stdout

# %%
ls_output.communicate(timeout=.1)

# %%
# !srun --help

# %%
