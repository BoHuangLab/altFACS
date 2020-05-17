"""
Hyperlog transformation for flow cytometry data.
The forward transformation refers to transforming the
raw data off the machine (i.e. a log transformation is the forword
and an exponential is its inverse).

Taken directly from FlowCytometryTools Package.

References:
Bagwell. Cytometry Part A, 2005.
Parks, Roederer, and Moore. Cytometry Part A, 2006.
Trotter, Joseph. In Current Protocols in Cytometry. John Wiley & Sons, Inc., 2001.
"""

from numpy import log10, sign, vectorize
from scipy.optimize import brentq


_machine_max = 2 ** 18
_l_mmax = log10(_machine_max)
_display_max = 10 ** 4


def _make_hlog_numeric(b, r, d):
    """
    Return a function that numerically computes the hlog transformation for given parameter values.
    """
    hlog_obj = lambda y, x, b, r, d: hlog_inv(y, b, r, d) - x
    find_inv = vectorize(lambda x: brentq(hlog_obj, -2 * r, 2 * r,
                                          args=(x, b, r, d)))
    return find_inv


def hlog(x, b=500, r=_display_max, d=_l_mmax):
    """
    Base 10 hyperlog transform.
    Parameters
    ----------
    x : num | num iterable
        values to be transformed.
    b : num
        Parameter controling the location of the shift
        from linear to log transformation.
    r : num (default = 10**4)
        maximal transformed value.
    d : num (default = log10(2**18))
        log10 of maximal possible measured value.
        hlog_inv(r) = 10**d
    Returns
    -------
    Array of transformed values.
    """
    hlog_fun = _make_hlog_numeric(b, r, d)
    if not hasattr(x, '__len__'):  # if transforming a single number
        y = hlog_fun(x)
    else:
        n = len(x)
        if not n:  # if transforming empty container
            return x
        else:
            y = hlog_fun(x)
    return y


def hlog_inv(y, b=500, r=_display_max, d=_l_mmax):
    """
    Inverse of base 10 hyperlog transform.
    """
    aux = 1. * d / r * y
    s = sign(y)
    if s.shape:  # to catch case where input is a single number
        s[s == 0] = 1
    elif s == 0:
        s = 1
    return s * 10 ** (s * aux) + b * aux - s


