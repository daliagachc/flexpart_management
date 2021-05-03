# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo


# %%
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co
from useful_scit.imps import *

plt;
# %%


def lin_reg(x,y):
    from sklearn.linear_model import LinearRegression
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    c = model.intercept_
    m = model.coef_
    return dict(m=m,c=c,rr=r_sq)

def f(p, x):
    """Basic linear regression 'model' for use with ODR"""
    return (p[0] * x) + p[1]

def orthoregress(x, y):
    """Perform an Orthogonal Distance Regression on the given data,
    using the same interface as the standard scipy.stats.linregress function.
    Arguments:
    x: x data
    y: y data
    Returns:
    [m, c, nan, nan, nan]
    Uses standard ordinary least squares to estimate the starting parameters
    then uses the scipy.odr interface to the ODRPACK Fortran code to do the
    orthogonal distance calculations.
    """

    from scipy.odr import Model, Data, ODR
    from scipy.stats import linregress
    linreg = linregress(x, y)
    mod = Model(f)
    dat = Data(x, y)
    od = ODR(dat, mod, beta0=linreg[0:2])
    out = od.run()

    return list(out.beta) + [np.nan, np.nan, np.nan]
