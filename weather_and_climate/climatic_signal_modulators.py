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

#-----------------------#
# Import custom modules #
#-----------------------#
#TODO: NO MODULES TO IMPORT YET
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
    # Naturally, autocorrelation can be a useful tool for traders to utilize;
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
    
# TODO: definitu seinalea zuritzeko funtzioak
# def signal_whitening(data, method="classic"):
    
#     if method=="classic":
        
#     elif method=="sklearn":
        
#     elif method=="zca":
                
def polynomial_fitting_coefficients(x, y, poly_ord):
    polyCoeff_array = np.polyfit(x, y, poly_ord)
    return polyCoeff_array
    
def evaluate_polynomial(polynomial_coefficients, value2eval):
    evaluated_poly_value = np.polyval(polynomial_coefficients, value2eval)
    return evaluated_poly_value