#----------------#
# Import modules #
#----------------#

from pathlib import Path
import sys

import calendar

import numpy as np
import pandas as pd
import scipy.stats as ss

#-----------------------#
# Import custom modules #
#-----------------------#

# Import module that finds python tools' path #
home_PATH = Path.home()
sys.path.append(str(home_PATH))

import get_pytools_path
fixed_path = get_pytools_path.return_custom_path()

# Enumerate custom modules and their paths #
#------------------------------------------#

custom_mod1_path = f"{fixed_path}/arrays_and_lists"
custom_mod2_path = f"{fixed_path}/strings"  
custom_mod3_path = f"{fixed_path}/weather_and_climate"

# Add the module paths to the path variable #
#-------------------------------------------#

sys.path.append(custom_mod1_path)
sys.path.append(custom_mod2_path)
sys.path.append(custom_mod3_path)

# Perform the module importations #
#---------------------------------#

import array_handler
import array_numerical_operations
import climate_statistics
import climatic_signal_modulators
import consecutive_idx_statistics
import meteorological_variables
import string_handler

#----------------------------------------------------#
# Define imported module(s)´ function call shortcuts #
#----------------------------------------------------#

periodic_statistics = climate_statistics.periodic_statistics
windowSum = climate_statistics.windowSum

select_array_elements = array_handler.select_array_elements
sort_array_rows_by_column = array_handler.sort_array_rows_by_column
remove_elements_from_array = array_handler.remove_elements_from_array

count_consecutive = array_numerical_operations.count_consecutive

find_substring_index = string_handler.find_substring_index

count_consecutive_days_maxdata\
= consecutive_idx_statistics.count_consecutive_days_maxdata
count_consecutive_days_mindata\
= consecutive_idx_statistics.count_consecutive_days_mindata

polynomial_fitting_coefficients\
= climatic_signal_modulators.polynomial_fitting_coefficients
evaluate_polynomial = climatic_signal_modulators.evaluate_polynomial

meteorological_wind_direction\
= meteorological_variables.meteorological_wind_direction

#--------------------------#
# Define  custom functions #
#--------------------------#

# TODO: ea hau hobeago jar daitekeen
def calculate_biovars(tmax_monthly_climat, 
                      tmin_monthly_climat, 
                      prec_monthly_climat):
    
    """
    Function that calculates 19 bioclimatic variables
    based on already monthly climatologic data, for every horizontal grid point.
    
    Parameters
    ----------
    tmax_monthly_climat : numpy.ndarray
          Array containing the monthly climatologic maximum temperature data.
    tmin_monthly_climat : numpy.ndarray
          Array containing the monthly climatologic minimum temperature data.
    precip_dataset : numpy.ndarray
          Array containing the monthly climatologic precipitation data.
    
    Returns
    -------
    p : numpy.ndarray
          Array containing the bioclimatic data for the considered period.
          structured as (biovariable, lat, lon).
    """

    dimensions = tmax_monthly_climat.shape
    bioclim_var_array = np.zeros((19, dimensions[1], dimensions[2]))
     
    # tavg = (tmin_monthly_climat + tmax_monthly_climat) / 2
    tavg = np.mean((tmax_monthly_climat, tmin_monthly_climat), axis=0)
    range_temp = tmax_monthly_climat - tmin_monthly_climat
      
    # P1. Annual Mean Temperature
    bioclim_var_array[0,:,:] = np.mean(tavg, axis=0)
      
    # P2. Mean Diurnal Range(Mean(period max-min))
    bioclim_var_array[1,:,:] = np.mean(range_temp, axis=0)
      
    # P4. Temperature Seasonality (standard deviation)
    bioclim_var_array[3,:,:] = np.std(tavg, axis=0) # * 100
      
    # P5. Max Temperature of Warmest Period 
    bioclim_var_array[4,:,:] = np.max(tmax_monthly_climat, axis=0)
     
    # P6. Min Temperature of Coldest Period
    bioclim_var_array[5,:,:] = np.min(tmin_monthly_climat, axis=0)
      
    # P7. Temperature Annual Range (P5 - P6)
    bioclim_var_array[6,:,:] = bioclim_var_array[4,:,:] - bioclim_var_array[5,:,:]
      
    # P3. Isothermality ((P2 / P7) * 100)
    bioclim_var_array[2,:,:] = bioclim_var_array[1,:,:] / bioclim_var_array[6,:,:] * 100
      
    # P12. Annual Precipitation
    bioclim_var_array[11,:,:] = np.sum(prec_monthly_climat, axis=0)
      
    # P13. Precipitation of Wettest Period
    bioclim_var_array[12,:,:] = np.max(prec_monthly_climat, axis=0)
      
    # P14. Precipitation of Driest Period
    bioclim_var_array[13,:,:] = np.min(prec_monthly_climat, axis=0)
    
    # P15. Precipitation Seasonality(Coefficient of Variation) 
    # the "+1" is to avoid strange CVs for areas where the mean rainfall is < 1 mm)
    bioclim_var_array[14,:,:] = ss.variation(prec_monthly_climat+1, axis=0) * 100
    
    # precipitation by quarters (window of 3 months)
    wet = windowSum(prec_monthly_climat, N=3)
    
    # P16. Precipitation of Wettest Quarter
    bioclim_var_array[15,:,:] = np.max(wet, axis=0)
      
    # P17. Precipitation of Driest Quarter 
    bioclim_var_array[16,:,:] = np.min(wet, axis=0)
      
    # temperature by quarters (window of 3 months)
    tmp_qrt = windowSum(tavg, N=3) / 3
      
    # P8. Mean Temperature of Wettest Quarter
    wet_qrt = np.argmax(wet, axis=0)
    for i in range(dimensions[1]):
        for j in range(dimensions[2]):
            bioclim_var_array[7,i,j] = tmp_qrt[wet_qrt[i,j],i,j]
      
    # P9. Mean Temperature of Driest Quarter
    dry_qrt = np.argmin(wet, axis=0)
    for i in range(dimensions[1]):
        for j in range(dimensions[2]):
            bioclim_var_array[8,i,j] = tmp_qrt[dry_qrt[i,j],i,j]
    
    # P10 Mean Temperature of Warmest Quarter 
    bioclim_var_array[9,:,:] = np.max(tmp_qrt, axis=0)
      
    # P11 Mean Temperature of Coldest Quarter
    bioclim_var_array[10,:,:] = np.min(tmp_qrt, axis=0)
          
    # P18. Precipitation of Warmest Quarter 
    hot_qrt = np.argmax(tmp_qrt, axis=0)
    for i in range(dimensions[1]):
        for j in range(dimensions[2]):
            bioclim_var_array[17,i,j] = wet[hot_qrt[i,j],i,j]
     
    # P19. Precipitation of Coldest Quarter 
    cold_qrt = np.argmin(tmp_qrt, axis=0)
    for i in range(dimensions[1]):
        for j in range(dimensions[2]):
            bioclim_var_array[18,i,j] = wet[cold_qrt[i,j],i,j]
    
    print("Biovariables have been successfully computed")
    return bioclim_var_array


def calculate_WSDI(season_daily_tmax, tmax_threshold, min_consec_days):
    
    """
    Function that calculates the WSDI (Warm Spell Duration Index),
    
    Input data
    ----------
    season_daily_tmax : numpy.ndarray or pandas.Series
          Daily maximum temperature data of the corresponding season in units ºC.
    tmax_threshold : float
          Upper limit of the maximum temperature.
    min_consec_days : int
          Minimum consecutive days number.
    
    Returns
    -------
    WSDI : int
          Number of total days where at least a specified number of
          consecutive days exceeds certain percentile as a threshold.
    """

    WSDI = count_consecutive_days_maxdata(season_daily_tmax,
                                          tmax_threshold,
                                          min_consec_days)

    return WSDI


def calculate_SU(season_daily_tmax, tmax_threshold):
    
    """
    Function that calculates the SU (Summer Days).
    
    Parameters
    ----------
    season_daily_tmax : numpy.ndarray or pandas.Series
          Daily maximum temperature data of the corresponding season in units ºC.
    
    tmax_threshold : float
          Upper limit of the maximum temperature, preferably 25ºC.
    
    Returns
    -------
    SU : int
          Number of days in which the
          maximum temperature has risen above the threshold.
    """
    
    SU = count_consecutive_days_maxdata(season_daily_tmax, tmax_threshold)

    return SU


def calculate_CSU(season_daily_tmax, tmax_threshold):
    
    """
    Function that calculates the CSU (Consecutive Summer Days).
    
    Parameters
    ----------
    season_daily_tmax : numpy.ndarray or pandas.Series
          Daily maximum temperature data of the season in units ºC.
    
    tmax_threshold : float
          Upper limit of the maximum temperature, preferably 25ºC.
    
    Returns
    -------
    CSU : int
          Number of maximum consecutive days in which
          the temperature has risen above the threshold.
    """
    
    CSU = count_consecutive_days_maxdata(season_daily_tmax,
                                         tmax_threshold,
                                         min_consec_days=None,
                                         calculate_max_consecutive_days=True)

    return CSU


def calculate_FD(season_daily_tmin, tmin_threshold):
    
    """
    Function that calculates the FD (Frost Days).
    
    Parameters
    ----------
    season_daily_tmin : numpy.ndarray or pandas.Series
          Daily minimum temperature data of the corresponding season in units ºC.
    
    tmin_threshold : float
          Upper limit of the minimum temperature, preferably 0ºC.
    
    Returns
    -------
    FD : int
          Number of days in which the
          minimum temperature has fallen below the threshold.
    """
    
    FD = count_consecutive_days_mindata(season_daily_tmin, tmin_threshold)

    return FD


def calculate_TN(season_daily_tmin, tmin_threshold):
    
    """
    Function that calculates the TN (Tropical Night Days).
    
    Parameters
    ----------
    season_daily_tmin : numpy.ndarray or pandas.Series
          Daily minimum temperature data of the corresponding season in units ºC.
    
    tmin_threshold : float
          Lower limit of the minimum temperature, preferably 20ºC.
    
    Returns
    -------
    TN : int
          Number of nights in which the
          minimum temperature has risen above the threshold.
    """
    
    TN = count_consecutive_days_mindata(season_daily_tmin,
                                        tmin_threshold,
                                        threshold_mode="above")
    return TN


def calculate_RR(season_daily_precip, precip_threshold):
    
    """
    Function that calculates the RR parameter (Wet Days).
    It is defined as the number of days in which the precipitation
    amount exceeds 1 mm.
    
    Parameters
    ----------
    season_daily_precip : numpy.ndarray or pandas.Series
          Daily precipitation data of the corresponding season in units mm.
    
    precip_threshold : float
          Upper limit of the daily precipitation, 1 mm in this case.
    
    Returns
    -------
    RR : int
          Number of days in which the
          precipitation has risen above the threshold.   
    """
    
    RR = count_consecutive_days_maxdata(season_daily_precip, precip_threshold)
    return RR


def calculate_CWD(season_daily_precip, precip_threshold):
    
    """
    Function that calculates the CWD (Consecutive Wet Days),
    i.e. the number of maximum consecutive days in which
    the precipitation amount exceeds 1 mm.
    
    Parameters
    ----------
    season_daily_precip : numpy.ndarray or pandas.Series
          Daily precipitation data of the season in units mm.
    
    precip_threshold : float
          Upper limit of the daily precipitation, 1 mm in this case.
    
    Returns
    -------
    CWD : int
          Number of maximum consecutive days in which
          the precipitation has risen above the threshold.
    """
    
    CWD = count_consecutive_days_maxdata(season_daily_precip,
                                         precip_threshold,
                                         min_consec_days=None,
                                         calculate_max_consecutive_days=True)

    return CWD


def calculate_HWD(tmax_array, tmin_array,
                  max_threshold, min_threshold,
                  date_array, min_consec_days):
    
    """
    Function that returns the total number of heat waves, based on daily data.
    A heat wave is defined such that at least in N consecutive days
    the maximum temperature exceeds its 95th percentile
    and the minimum temperature exceeds it 90th percentile.
    
    Each heat wave is assocciated with the following:
    
    -Heat wave intensity : maximum temperature registered during the heat wave,
                            i.e. that event satisfying the conditions aforementioned.
    -Heat wave duration : number of consecutive days of the heat wave.
    -Heat wave global intensity : sum of the maximum temperatures registered
                                  during the heat wave,
                                  divided by its duration.
    
    Parameters
    ----------
    tmax_array : numpy.ndarray or pandas.Series
          An array which contains the daily maximum temperature data.
    tmin_array : numpy.ndarray or pandas.Series
          An array which contains the daily minimum temperature data.
    max_threshold : float
          Upper limit.
    min_threshold : float
          Lower limit.
    date_array : pandas.DatetimeIndex
          Array containing dates, in this case of the corresponding season.
    min_consec_days : int
          Minimum consecutive days number.
    
    Returns
    -------
    HWD_characteristics : numpy.ndarray composed of tuples
          All heat wave events,
          each with its characteristics englobed in a tuple.
    HWD : int 
          Total number of heat wave events.
    """

    N = min_consec_days
    satisfied_thres_bool_arr = (tmax_array > max_threshold) * (tmin_array > min_threshold)
           
    HWD_characteristics = []
    HWD = 0 

    block_consecutive_idx = np.flatnonzero(
                            np.convolve(satisfied_thres_bool_arr,
                                        np.ones(N, dtype=int),
                                        mode='valid')>=N)
    
    
    consec_nums_on_consecutive_idx = count_consecutive(block_consecutive_idx)
    
    if consec_nums_on_consecutive_idx and len(consec_nums_on_consecutive_idx) >= 1:
        
        hw_events_NdayMultiply = consec_nums_on_consecutive_idx.copy()
                
        for i in range(len(hw_events_NdayMultiply)):
            hw_event_partial = block_consecutive_idx[:hw_events_NdayMultiply[i]]

            hw_event = np.unique(np.append(hw_event_partial,
                                           np.arange(hw_event_partial[-1],
                                                     hw_event_partial[-1]+N)))
            
            hw_event_MaxTemps = tmax_array[hw_event]
    
            hw_event_global_intensity = sum(hw_event_MaxTemps) / len(hw_event)
            hw_event_duration = len(hw_event)
            hw_event_intensity = np.max(hw_event_MaxTemps)
            
            hw_event_characteristics = (hw_event_duration,
                                        hw_event_global_intensity,
                                        hw_event_intensity,
                                        date_array[hw_event[0]])
            
            HWD_characteristics.append(hw_event_characteristics)
            HWD += hw_event_characteristics[0]
            idx_to_delete = [idx[0] for idx in enumerate(hw_event_partial)]
    
            block_consecutive_idx = np.delete(block_consecutive_idx,
                                              idx_to_delete)

        return HWD_characteristics, HWD
        
    else:
        HWD_characteristics = (0, None, None, None)
        return HWD_characteristics, 0

# TODO: indexazioa azkar liteke?

def calculate_HDY(hourly_df,
                  varlist,
                  varlist_primary,
                  drop_date_idx_col=False,
                  drop_new_idx_col=True):
    """
    Function to calculate the ´Hourly Design Year´,
    based on the ISO 15927-4 2005 (E) standard,
    version of January 2021.
    """
    
    #--------------------------#
    # Define the HDY dataframe #
    #--------------------------#

    HDY_df = pd.DataFrame(columns = varlist)

    # Define input HDY parameters #
    #-----------------------------#

    hist_years = pd.unique(hourly_df.date.dt.year)
    lhy = len(hist_years)
    
    months = pd.unique(hourly_df.date.dt.month)
    month_names = list(calendar.month_abbr)
    month_names.remove(month_names[0])

    #-----------------------------------------------------#
    #                     PROGRAM CORE                    #
    # Implementation of the ISO-15927-4 2005 (E) standard #
    #         Hourly Design Year (HDY) computation        #
    #-----------------------------------------------------#

    lowest_total_rank_year_list = []
     
    # Define the HDY dataframe #
    HDY_df = pd.DataFrame(columns = varlist)
     
    # Perform ISO 15927-4 2005 (E) standard steps #
    #---------------------------------------------#
    
    print("\nPerforming ISO 15927-4 2005 (E) standard steps...\n")
     
    for m in months:

        hdata_MONTH = hourly_df[hourly_df.date.dt.month == m].filter(items = varlist_primary)\
                      .reset_index(drop=drop_new_idx_col)
     
        # Step a) #
        
        """The first key MUST BE ´date´ """
        varlist_prim_rank_phi = [varlist_primary[0]]
        
        for var in varlist_primary[1:]:
            for i in range(3):
                if i==0:
                    varlist_prim_rank_phi.append(var)
                    
                elif i==1:
                    var_rank = var + "_rank"
                    varlist_prim_rank_phi.append(var_rank)
                
                elif i==2:
                    var_phi = var + "_phi"
                    varlist_prim_rank_phi.append(var_phi)
                                
        try:
            hdata_MONTH_dm\
            = periodic_statistics(hdata_MONTH, 'mean', 'D', drop_date_idx_col)
        except:
            hdata_MONTH.loc[:,varlist_primary[1:]]\
            = hdata_MONTH.loc[:,varlist_primary[1:]].apply(pd.to_numeric)
        
        hdata_MONTH_dm \
        = periodic_statistics(hdata_MONTH, 'mean', 'D', drop_date_idx_col)
        
        hdata_MONTH_dm_bymonth = hdata_MONTH_dm[hdata_MONTH_dm.date.dt.month == m]\
                                 .reset_index(drop=drop_new_idx_col)
     
        hdata_MONTH_rank_phi = pd.DataFrame(hdata_MONTH_dm_bymonth, 
                                            columns = varlist_prim_rank_phi)
        records_MONTH_dm_bymonth = len(hdata_MONTH_dm_bymonth)
        
        # Step b) #
        no_of_days = len(pd.unique(hdata_MONTH_rank_phi.date.dt.day))
     
        vars_rank = [var 
                     for var in varlist_prim_rank_phi 
                     if "rank" in var]
        dict_rank = {}
     
        vars_phi = [var 
                    for var in varlist_prim_rank_phi 
                    if "phi" in var]
        dict_phi = {}
     
        lv = len(hdata_MONTH.columns)-1
     
        for iv in range(lv):
            dict_rank[vars_rank[iv]] = []
            sorted_var = np.sort(hdata_MONTH_rank_phi[varlist_primary[1:][iv]])
        
            for i in range(records_MONTH_dm_bymonth):
                where = np.where(hdata_MONTH_rank_phi\
                                 [varlist_primary[1:][iv]].loc[i] == sorted_var)[0][0]
                dict_rank[vars_rank[iv]].append(where)
            
            dict_rank[vars_rank[iv]] = np.array(dict_rank[vars_rank[iv]])+1
            hdata_MONTH_rank_phi[vars_rank[iv]] = dict_rank[vars_rank[iv]]
     
     
        for iv in range(lv):
            dict_phi[vars_phi[iv]] = dict_rank[vars_rank[iv]]/(lhy*no_of_days+1)    
            hdata_MONTH_rank_phi[vars_phi[iv]] = dict_phi[vars_phi[iv]]   
        
        # Step c) #
        dict_ym = {}
     
        for var in varlist_primary[1:]:
            dict_ym[var] = {}
     
        for iv in range(lv):
            for y in hist_years:
                    
                hdata_MONTH_ym = hdata_MONTH_rank_phi[(hdata_MONTH_rank_phi.date.dt.year == y)
                                                      & (hdata_MONTH_rank_phi.date.dt.month == m)]
                items = ["date",varlist_primary[1:][iv]]
        
                hdata_MONTH_ym_var_sel = hdata_MONTH_ym.filter(items = items)\
                                        .reset_index(drop=drop_new_idx_col)
               
                
                # Perform the ranking #                       
                no_of_days = len(hdata_MONTH_ym_var_sel)
              
                var_orig = hdata_MONTH_ym_var_sel[varlist_primary[1:][iv]]
                var_sorted = np.sort(var_orig)
                var_rank = []
                
                for i in range(no_of_days):
                    where = np.where(var_orig[i] == var_sorted)[0][0]
                    var_rank.append(where)                
                 
                
                var_rank = np.array(var_rank)+1
                F = var_rank/(no_of_days+1)
                
                next_df = pd.DataFrame(var_rank,columns = ['rank'])
                hdata_MONTH_ym_var_sel = pd.concat([hdata_MONTH_ym_var_sel,next_df],axis = 1)
                
                next_df = pd.DataFrame(F,columns = ['F'])
                hdata_MONTH_ym_var_sel = pd.concat([hdata_MONTH_ym_var_sel,next_df],axis = 1)       
                  
        # Step d) #
                Fs = []
                for i in range(no_of_days):
                    where = np.where(
                        hdata_MONTH_ym_var_sel.loc[i].date == hdata_MONTH_rank_phi.date
                        )[0][0]
                    phi = hdata_MONTH_rank_phi.loc[where,vars_phi[iv]]
                    Fs_val = abs(hdata_MONTH_ym_var_sel.loc[i].F-phi)
                    Fs.append(Fs_val)
                        
                next_df = pd.DataFrame(np.array(Fs),columns = ['Fs'])
                hdata_MONTH_ym_var_sel = pd.concat([hdata_MONTH_ym_var_sel,next_df],axis = 1)  
                        
                dict_ym[varlist_primary[1:][iv]][(y,m)] = hdata_MONTH_ym_var_sel
                
        # Step e) #
        varlist_Fssum_rank = ["Year"]
        
        for var in varlist_primary[1:]:
            for i in range(2):
                if i==0:
                    var_Fs_sum=var+"_Fs_sum"
                    varlist_Fssum_rank.append(var_Fs_sum)
                elif i==1:
                    var_Fs_sum_rank=var+"_Fs_sum_rank"
                    varlist_Fssum_rank.append(var_Fs_sum_rank)
        
        lvfsr = len(varlist_Fssum_rank)
     
        Fs_sum_df = pd.DataFrame(columns = varlist_Fssum_rank)
        Fs_sum_df.Year = hist_years
     
        dict_ym_Fs_sum = {}
        for iv in range(1,lvfsr,2):
            dict_ym_Fs_sum[varlist_Fssum_rank[iv]] = {}
            for y in hist_years:
                dict_ym_Fs_sum[varlist_Fssum_rank[iv]][(y,m)] = 0
     
        for iv in range(1,lvfsr,2):
            Fs_sum = []
            for y in hist_years:
                dict_ym_Fs_sum[varlist_Fssum_rank[iv]][(y,m)]\
                += np.sum(dict_ym[varlist_primary[iv//2+1]][(y,m)].Fs)
                
                Fs_sum.append(dict_ym_Fs_sum[varlist_Fssum_rank[iv]][(y,m)])
     
            Fs_sum_df[varlist_Fssum_rank[iv]] = np.array(Fs_sum)
        
     
        for iv in range(1,lvfsr,2):
            Fs_sum_orig = Fs_sum_df[varlist_Fssum_rank[iv]]
            Fs_sum_sorted = np.sort(Fs_sum_orig)
        
            Fs_sum_rank = []
            for i in range(lhy):
                where = np.where(Fs_sum_orig[i] == Fs_sum_sorted)[0][0]
                Fs_sum_rank.append(where)
            
            Fs_sum_df[varlist_Fssum_rank[iv+1]] = np.array(Fs_sum_rank)+1
        
        # Step f) #    
        rank_sum = np.zeros(lhy,'d')
        for iv in range(2,lvfsr,2):
            rank_sum +=  Fs_sum_df[varlist_Fssum_rank[iv]].values
     
        next_df = pd.DataFrame(rank_sum.astype(np.int64),columns = ["total_rank"])
        Fs_sum_df = pd.concat([Fs_sum_df,next_df],axis = 1)
     
        # Step g) #
        Fs_sum_df_sorted_total_rank = pd.DataFrame(
            sort_array_rows_by_column(Fs_sum_df.values,-1),
            columns = Fs_sum_df.columns
            ).filter(items = ['Year','total_rank']).astype(np.int64)
        Fs_sum_df_sorted_total_rank.columns = ['Year','total_rank_sorted']
     
        """
         Method to choose the HDY_df
         ------------------------
        
        ·Original method is to calculate the monthly mean wind speed of each month
         of the three lowest total rank set, together with the climatology
         of the corresponding month, to then compute the anomalies.
        ·For this study, take the year which has the lowest total rank,
         governed by the primary variables,
         and select the original hourly data for that month and year.
        """
     
        lowest_total_rank_year = Fs_sum_df_sorted_total_rank.loc[0].Year
        lowest_total_rank_year_list.append(lowest_total_rank_year)
        print("Design year component: ",lowest_total_rank_year,month_names[m-1])
           
        hourly_data_sel = hourly_df[(hourly_df.date.dt.year == lowest_total_rank_year)
                                    &(hourly_df.date.dt.month == m)]
        
        HDY_df = pd.concat([HDY_df,hourly_data_sel], axis = 0)
       
    HDY_df = HDY_df.reset_index(drop=drop_new_idx_col)    
    HDY_years = lowest_total_rank_year_list.copy()
    return HDY_df, HDY_years


# TODO: behekoa ez da behin betikoa, aldagai bakoitzeko interpolaketa-metodoen
# iradokizun asko baitago
def HDY_interpolation(HDY_df,
                      HDY_years,
                      previous_month_last_time_range,
                      next_month_first_time_range,
                      varlist_to_interpolate,
                      polynomial_order,
                      drop_date_idx_col=False):
    
    """
    Interpolates along a selected time array between two months
    of and HDY constructed following the standard ISO 15927-4 2005 (E).
    
    Since the HDY is composed of 'fragments' of completely different months
    there are unavoidable vertical jumps on the tendencies for every variable.         
    Interpolation will help to smoothen those jumps.
    
    The problem is that the slice to be interpolated
    in most of the cases presents vertical jumps,
    so when interpolating that slice those jumps won't be completely removed.
    
    In this case, the polynomial fitting technique will be applied.
    This function performs a determined order polynomial interpolation,
    passed as an argument.
    
    Do not consider the whole previous and next month
    of the slice to be interpolated, but only some days more earlier and later.
    The reason for that is because data is hourly so there are
    obviously a lot of oscillations.
    
    Also do not consider all month indexes,
    because the last interpolation involving pairs of months
    is that of October and November.
    
    For practicity and uniqueness purposes, it is strongly reccommended,
    to the extent of present elements in the variable list
    to interpolate against, to follow these standard short names.
    The order of the variables is not strict:
    
    2 metre temperature : t2m
    2 metre dew point temperature : d2m
    Relative humidity : rh
    10 metre U wind component : u10
    10 metre V wind component : v10
    10 metre wind speed modulus : ws10
    Surface solar radiation downwards : ssrd
    Surface thermal radiation downwards : strd
    Surface solar radiation downwards : ssrd
    Direct solar radiation at the surface : fdir
    Diffuse solar radiation at the surface : fdif
    Surface pressure : sp
    
    
    Notes
    -----
    Both wind direction and speed modulus will be calculated
    after the interpolation of u10 and v10 arrays.
    """
    
    HDY_interp = HDY_df.copy()
    
    HDY_months = pd.unique(HDY_interp.date.dt.month)
    lhdy_m = len(HDY_months) # == len(HDY_years), by definition
    
    # Remove ´ws10´ variable from the list of variables to be interpolated #
    ws10_idx = find_substring_index(varlist_to_interpolate, "ws10")
    varlist_to_interpolate = remove_elements_from_array(varlist_to_interpolate, 
                                                        ws10_idx)

    for i in range(lhdy_m-1):
    
        days_slice_prev\
        = pd.unique(HDY_interp[(HDY_interp.date.dt.year == HDY_years[i])
                        &(HDY_interp.date.dt.month == HDY_months[i])].date.dt.day)
        
        days_slice_next\
        = pd.unique(HDY_interp[(HDY_interp.date.dt.year == HDY_years[i+1])
                        &(HDY_interp.date.dt.month == HDY_months[i+1])].date.dt.day)
        
        pmltr = np.array(previous_month_last_time_range.split("-"), "i")
        pmltr1 = pmltr[0]
        pmltr2 = pmltr[-1]
        
        nmftr = np.array(next_month_first_time_range.split("-"), "i")
        nmftr1 = nmftr[0]
        nmftr2 = nmftr[-1]
    
        ymdh_first1\
        = f"{HDY_years[i]:04d}-{HDY_months[i]:02d}-{days_slice_prev[-1]:02d} "\
          f"T{pmltr1:02d}"
          
        ymdh_last1\
        = f"{HDY_years[i]:04d}-{HDY_months[i]:02d}-{days_slice_prev[-1]:02d} "\
          f"T{pmltr2:02d}"
          
        ymdh_first2\
        = f"{HDY_years[i+1]:04d}-{HDY_months[i+1]:02d}-{days_slice_next[0]:02d} "\
          f"T{nmftr1:02d}"
          
        ymdh_last2\
        = f"{HDY_years[i+1]:04d}-{HDY_months[i+1]:02d}-{days_slice_next[0]:02d} "\
          f"T{nmftr2:02d}"
        
        df_slice1 = HDY_interp[(HDY_interp.date >= ymdh_first1)&
                               (HDY_interp.date <= ymdh_last1)]
        df_slice2 = HDY_interp[(HDY_interp.date >= ymdh_first2)&
                               (HDY_interp.date <= ymdh_last2)]
    
        df_slice_to_fit_reidx\
        = pd.concat([df_slice1, df_slice2],axis=0).reset_index(drop=drop_date_idx_col)
        
        # Polynomial fitting parameters #
        poly_ord = polynomial_order
        x = np.arange(len(df_slice_to_fit_reidx))
        df_slice_fit_indices = np.array(df_slice_to_fit_reidx.index)
        
        for var in varlist_to_interpolate:
            y_var = df_slice_to_fit_reidx[var]
            var_poly_coeffs = polynomial_fitting_coefficients(x, y_var, poly_ord)    
            
            for ix in range(len(x)):
                var_eval = evaluate_polynomial(var_poly_coeffs, x[ix])
                df_slice_to_fit_reidx.loc[df_slice_fit_indices[ix],var] = var_eval
                
                idx_for_hdy = df_slice_to_fit_reidx.loc[df_slice_fit_indices[ix],"index"]
                df_slice_to_fit_reidx.loc[df_slice_to_fit_reidx["index"] == idx_for_hdy,var]\
                = var_eval            
                HDY_interp.loc[idx_for_hdy,var] = var_eval
                    
                
    # Calculate the 10m wind speed direction and modulus #
    """
    On the wind direction calculus
    ------------------------------
    
    ·The sign of both components follow the standard convention:
        * u is positive when the wind is westerly,
          i.e wind blows from the west and is eastwards.
        * v is positive when the wind is northwards,
          i.e wind blows from the south.
          
    ·From the meteorological point of view,
     the direction of the wind speed vector is taken as
     the antiparallel image vector.
     The zero-degree angle is set 90º further than the
     default unit cyrcle, so that 0º means wind blowing from the North. 
    """    
    HDY_interp.loc[:,"ws10"]\
    = np.sqrt(HDY_interp.u10 ** 2 + HDY_interp.v10 ** 2)
    
    print("\nCalculating the wind direction from the meteorological point of view...")
    
    wind_dir_meteo_interp = meteorological_wind_direction(HDY_interp.u10.values,  
                                                               HDY_interp.v10.values)

    return HDY_interp, wind_dir_meteo_interp
