# -*- coding: utf-8 -*-
"""
@author: eilan_dk (dirk.eilander@deltares.nl)
v0.1 18/08/2016

"""

#----------------#
# Import modules #
#----------------#

import numpy as np
from scipy.stats.mstats import mquantiles
from scipy.interpolate import interp1d

#-------------------------#
# Define custom functions #
#-------------------------#

def basic_bias_correction(obs, p, s, method='delta', nbins=10, extrapolate=None):
    """Bias Correction techniques for correcting simulated output based on differences between the CDFs of
    observed and simulated output for a training period.

    three different methods are available
    'delta'   This is the simplest bias correction method, which consists on adding the mean change signal
              to the observations (delta method). This method corresponds to case g=1 and f=0 in Amengual
              et al. (2012). This method is applicable to any kind of variable but it is preferable not to
              apply it to bounded variables (e.g. precipitation, wind speed, etc.) because values out of
              range could be obtained.
    'scaling' This method is very similar to the delta method but, in this case, the correction consist on
              scaling the simulation with the difference (additive: 'scaling_add') or quotient
              (multiplicative: 'scaling_multi') between the mean of the observations and the simulation in
              the train period.
    'eqm'     Empirical Quantile Mapping (eQM) This is the most popular bias correction method which consists
              on calibrating the simulated Cumulative Distribution Function (CDF) by adding to the observed
              quantiles both the mean delta change and the individual delta changes in the corresponding
              quantiles. This is equivalent to f=g=1 in Amengual et al. (2012). This method is applicable to
              any kind of variable.

    input args
    obs:      observed climate data for the training period
    p:        simulated climate by the model for the same variable obs for the training period.
    s:        simulated climate for the variables used in p, but considering the test/projection period.
    method:   'delta', 'scaling_add', 'scaling_multi', 'eqm', see explenation above
    nbins:    for 'eqm' method only: number of quantile bins in case of 'eqm' method (default = 10)
    extrapolate: for 'eqm' method only: None (default) or 'constant' indicating the extrapolation method to
              be applied to correct values in 's' that are out of the range of lowest and highest quantile of 'p'

    output
    c:        bias corrected series for s


    ref:
    Amengual, A., Homar, V., Romero, R., Alonso, S., & Ramis, C. (2012). A statistical adjustment of regional
    climate model outputs to local scales: application to Platja de Palma, Spain. Journal of Climate, 25(3), 939-957.
    http://journals.ametsoc.org/doi/pdf/10.1175/JCLI-D-10-05024.1

    based on R-package downscaleR, source:
    https://github.com/SantanderMetGroup/downscaleR/wiki/Bias-Correction-and-Model-Output-Statistics-(MOS)

    TODO: include conditioning on weather types to alleviate the problem that arise when the dry day frequency changes.
    """

    if (method == 'eqm') and (nbins > 1):
        binmid = np.arange((1./nbins)*0.5, 1., 1./nbins)
        qo = mquantiles(obs[np.isfinite(obs)], prob=binmid)
        qp = mquantiles(p[np.isfinite(p)], prob=binmid)
        p2o = interp1d(qp, qo, kind='linear', bounds_error=False)
        c = p2o(s)
        if extrapolate is None:
            c[s > np.max(qp)] = qo[-1]
            c[s < np.min(qp)] = qo[0]
        elif extrapolate == 'constant':
            c[s > np.max(qp)] = s[s > np.max(qp)] + qo[-1] - qp[-1]
            c[s < np.min(qp)] = s[s < np.min(qp)] + qo[0] - qp[0]

    elif method == 'delta':
        c = obs + (np.nanmean(s) - np.nanmean(p))

    elif method == 'scaling_add':
        c = s - np.nanmean(p) + np.nanmean(obs)

    elif method == 'scaling_multi':
        c = (s/np.nanmean(p)) * np.nanmean(obs)

    else:
        raise ValueError("incorrect method, choose from 'delta', 'scaling_add', 'scaling_multi' or 'eqm'")

    return c


def apply_monthly_deltas(var_string,
                         time_var,
                         historical_ds,
                         delta_ds,
                         times_fut,
                         basic_operator):
    
    # Function that applies data corresponding to future monthly deltas
    # to the whole set of historical data. It works with xarray data sets.
    # 
    # Parameters
    # ----------
    # var_string : str
    #       String used to identify the variable to work with.
    # time_var : str
    #       String used to identify the time variable.
    # historical_ds : xarray.core.dataset.Dataset
    #       Xarray data set containing historical data.
    # delta_ds : xarray.core.dataset.Dataset
    #       Xarray data set containing data
    #       corresponding to future deltas.
    # times_fut : pandas.core.indexes.datetimes.DatetimeIndex
    #       Pandas time slice corresponding to a future period of time.
    # basic_operator : {"+", "-", "*", "/"}
    #       
    # Returns
    # -------
    # ds_proj : xarray.core.dataset.Dataset
    #       Data set containing projected data for passed variable string.
    
    times_hist = historical_ds[time_var].values
    
    records_hist = len(times_hist)    
    records_fut = len(times_fut)
            
    for mon in range(1,13):
        historical_ds_bymonth\
        = historical_ds.sel(time=historical_ds[time_var].dt.month==mon)
        delta_ds_bymonth\
        = delta_ds.sel(time=delta_ds[time_var].dt.month==mon)
        
        if basic_operator == "+":
            res_bymonth = historical_ds_bymonth + delta_ds_bymonth[var_string].values
        elif basic_operator == "-":
            res_bymonth = historical_ds_bymonth - delta_ds_bymonth[var_string].values
        elif basic_operator == "*":
            res_bymonth = historical_ds_bymonth * delta_ds_bymonth[var_string].values
        elif basic_operator == "/":
            res_bymonth = historical_ds_bymonth / delta_ds_bymonth[var_string].values
        else:
            raise ValueError("Wrong basic operator chosen.")
        
        historical_ds.loc[dict(time=historical_ds[time_var].dt.month==mon)]\
        = res_bymonth
        
        """Some time array lengths do not exactly match,
        but it is pointless to adapt sort of
        equivalent future time arrays.
        Then, for the updated historical xarray data set,
        the length-matching future time array will be directly assigned.
        """
        
        length_matching_idx = min(records_hist, records_fut)
        historical_ds.update(dict(time=times_fut[:length_matching_idx]))
        
    projected_ds = historical_ds.copy()
    return projected_ds

# TODO: definitu delta-zuzenketa sinplea, non soilik etorkizuneko
# eta iraganeko ausazko bi datu-sorta erabiltzen diren, proiekzioak
# edo behaketak direnentz bereizi gabe.
