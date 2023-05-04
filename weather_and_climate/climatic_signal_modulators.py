#----------------#
# Import modules #
#----------------#

# import importlib
from pathlib import Path

import numpy as np
import scipy.signal as ssig

#---------------------------#
# Get the fixed directories #
#---------------------------#

cwd = Path.cwd()
main_path = Path("/".join(cwd.parts[:3])[1:]).glob("*/*")

# All-code containing directory #
fixed_dirpath = str([path
                     for path in main_path
                     if "pytools" in str(path).lower()][0])

#------------------#
# Define functions #
#------------------#

def autocorrelate(x, twosided=False):
    
    # Function that calculates the autocorrelation of a time series.
    #
    # Adapted from https://www.investopedia.com/terms/a/autocorrelation.asp
    # ---------------------------------------------------------------------
    # Autocorrelation is a mathematical representation
    # of the degree of similarity between a given time series
    # and a lagged version of itself over successive time intervals.
    # 
    # It's conceptually similar to the correlation between
    # two different time series,
    # but autocorrelation uses the same time series twice:
    # Once in its original form and once lagged one or more time periods. 
    # 
    # For example, if it's rainy today, the data suggests that it's more likely
    # to rain tomorrow than if it's clear today.
    # When it comes to investing, a stock might have a
    # strong positive autocorrelation of returns,
    # suggesting that if it's "up" today,
    # it's more likely to be up tomorrow, too.
    # 
    # Of course, autocorrelation can be a useful tool for traders to utilize;
    # particularly for technical analysts.
    #  
    # Adapted from https://stackoverflow.com/questions/643699/how-can-i-use-numpy-correlate-to-do-autocorrelation
    # -----------------------------------------------------------------------------------------------------------
    # 
    # At a time difference of 0,
    # the auto-correlation should be the highest
    # because the signal is identical to itself,
    # so it its expected that the first element in the autocorrelation
    # result array would be the greatest.
    # 
    # The definition implies sums for all lags (not strictly times),
    # so it is performed from tau in [-inf, inf] (two sided).
    # Usually one is only interested on the series from lags
    # tau in [0, inf].
    # 
    # Apart from these explanations, it is important to notice that,
    # the definition involves the calculation of the expected value
    # of the simple deviation, i.e. value at lag tau minus the series mean.
    # 
    # The function uses numpy.correlate module by default.
    # 
    # Parameters
    # ----------
    # x : list or numpy.array
    #       Object containing certain variable's data.
    # twosided : bool
    #       If it is False, then only autocorrelation ranging from 
    #       lags [0, infinity] is calculated,
    #       otherwise from lags [-infinity, infinity].
    # 
    # Returns
    # -------
    # x_autocorr : numpy.ndarray
    #       Array containing autocorrelation values.
    # 
    # Note
    # ----
    # Checked experimentally. For large arrays (>~75000) according to
    # numpy documentation, it is preferable to use scipy.signal.correlate
    # since it uses Fourier methods, which makes the computation way faster.
    # NEITHER numpy.correlate nor scipy.signal.correlate ignore NaN values,
    # so they have to be removed previously.
    
    x_nonan = x[~np.isnan(x)]
    x_demean = x_nonan - np.mean(x_nonan)
    lx = len(x_demean)
    
    if lx <= int(5e4):
        x_autocorr = np.correlate(x_demean, x_demean, mode="full")
    else:
        x_autocorr = ssig.correlate(x_demean, x_demean)
    
    x_autocorr_norm = x_autocorr / np.max(x_autocorr)
    
    if twosided:
        return x_autocorr_norm
    else:
        x_autocorr_onesided = x_autocorr_norm[x_autocorr_norm.size//2:] 
        return x_autocorr_onesided
    
    
def polynomial_fitting(y, poly_ord, fix_edges=False, 
                       poly_func=None, poly_params=None):
    
    # Performs the polynomial fitting over a 1D array,
    # using the least squares fit method.
    # 
    # This fitting method tries to fit a curve with a polynomial
    # p(x) = p[0] * x**deg + ... + p[deg] of degree 'deg' to points (x, y).
    # 
    # For that, returns a vector of coefficients p that minimises
    # the squared error in the order deg, deg-1, ... 0,
    # 
    # A lot of examples include pre-selected x-points that are passed into
    # function numpy.polyfit, but as far as I am concerned,
    # it is more practical to simply construct a linear space,
    # between the edges of the array to be fitted.
    # 
    # Having this vector of coefficients, it then emulates the
    # mentioned polynomial to encapsulate "natural" operations on polynomials.
    # In simpler words, it constructs the polynomial as in written form, 
    # that is, including the unknown variable.
    # In this way, the array is fitted by evaluating it over the
    # best fitting polynomial.
    # 
    # Parameters
    # ----------
    # y : list or np.ndarray
    #       y-coordinates of the sample points. It must be 1D, otherwise
    #       the function flattens the object to 1D.
    # poly_ord : int 
    #       The order of the array-fitting polynomial
    # fix_edges : bool
    #       If True, after performing the interpolation, the original
    #       edges of array 'y' will be maintained,
    #       for that making the following substitution:
    #           ·new_y[0] = y[0]      
    #           ·new_y[-1] = y[-1] 
    # 
    # poly_func : function
    #       An alternative that consists of a function
    #       with a predefined polynomial.
    #       If is not None, then  the'scipy.optimize' module's 'curve_fit' 
    #       function is used.
    #       An example of this function would be, 
    #       for the case of a 4th order polynomial:
    # 
    #           ·def func(x, a, b, c, d, e):
    #                return a*x**3 + b*x**2 + c*x + d,
    #       
    #       where 'x' is a vector.
    # 
    # poly_params : list of integers or dictionary of integers
    #       Used to pass the parameters into the latter.
    #       An example linked with the mentioned 'func' function would be:
    # 
    #       ·params = dict(a=0.6, b=0.15, c=0.2, d=0.7)
    # 
    # Returns
    # -------
    # new_y : np.ndarray
    #        Polynomial fitted value containing array.
    # 
    # Note
    # ----
    # The inconvenience of choosing the 'curve_fit' method it that the user
    # has to define the function manually and adjust the parameters
    # depending on the quality of the curve fitting.
    
    y_shape = y.shape
    if len(y_shape) > 1:
        y = y.flatten()
    
    ly = len(y)
    x = np.arange(ly)
    
    if poly_func is None:
        x_linspace = np.linspace(x[0], x[-1])

        coefficients = np.polyfit(x, y, poly_ord)
        polynomial = np.poly1d(coefficients)
        new_y = polynomial(x_linspace)
        
    else:
        from scipy.optimize import curve_fit
        
        y_polynomial = poly_func(y, **poly_params)
        popt, pcov = curve_fit(poly_func, x, y_polynomial)
        new_y = poly_func(x,*popt)
        
    if fix_edges:
        new_y_fixedEdges = new_y.copy()
        new_y_fixedEdges[0] = y[0]
        new_y_fixedEdges[-1] = y[-1]
        
        return new_y_fixedEdges
    
    else:
        return new_y
    
# TODO: definitu seinalea zuritzeko funtzioak
# def signal_whitening(data, method="classic"):
    
#     if method=="classic":
        
#     elif method=="sklearn":
        
#     elif method=="zca":
