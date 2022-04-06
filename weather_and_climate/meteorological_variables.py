#----------------#
# Import modules #
#----------------#

import numpy as np

#-------------------------#
# Define custom functions #
#-------------------------#

def ws_unit_converter(data, unit_converter):
    
    if unit_converter == "2ms":
        data_converted = data*5/18
        return data_converted
    
    elif unit_converter == "2kmh":
        data_converted = data*18/5
        return data_converted
    
    else:
        raise ValueError("Wrong unit converter. Options are {'2ms', '2kmh'}.")
        

def angle_converter(angle, method):

    if method == "deg2rad":
        radians = np.deg2rad(angle)
        return radians

    elif method == "rad2deg":
        degrees = np.rad2deg(angle)
        return degrees

    else:
        raise ValueError("Wrong unit converter. "
                         "Options are {'deg2rad', 'rad2deg'}.")
        

def meteorological_wind_direction(u, v):
    
    # Calculates the wind direction, as the opposite to
    # where the wind is blowing to. The 0 angle is located
    # at the middle top of the goniometric cyrcle.
    # This means that if the direction is, for example, 225º,
    # then that is where wind is blowing, thus coming from
    # an angle of 45º, so the wind is blowing from the north-east.
    # 
    # Parameters
    # ----------
    # u : numpy.ndarray
    #       Array containing the modulus and sense of the
    #       zonal component of the wind.
    # v : numpy.ndarray
    #       Array containing the modulus and sense of the
    #       meridional component of the wind.
    # 
    # Returns
    # -------
    # wind_dir_meteo_array : numpy.ndarray
    #       Array containing the directions of the wind, 
    #       described as in the first paragraph.
    
    if isinstance(u, int) or isinstance(v, int)\
        or isinstance(u, float) or isinstance(v, float):
        u = [u]
        v = [v]
            
    else:
        if u.dtype == 'O':
            u = u.astype('d')
        if v.dtype == 'O':
            v = v.astype('d')
    
    u_records = len(u)
    v_records = len(v)
    
    wind_dir_meteo_list = []
    
    if u_records == v_records:
        for t in range(u_records):  
            
            print(f"Calculating the wind direction for the time no. {t}...")
            
            if u[t] != 0 and v[t] != 0:
                wind_dir = angle_converter(np.arctan2(v[t],u[t]), "rad2deg")
                
                if u[t] > 0 and v[t] > 0:
                    wind_dir_meteo = 180 - (abs(wind_dir) - 90)
                    
                elif u[t] < 0 and v[t] > 0:
                    wind_dir_meteo = 180 - (wind_dir - 90)
                    
                elif u[t] > 0 and v[t] < 0:
                    wind_dir_meteo = 360 + wind_dir
                    
                elif u[t] < 0 and v[t] < 0:
                    wind_dir_meteo = 180 + wind_dir
                    
            elif u[t] == 0 and v[t] != 0:
                    
                if v[t] > 0:
                    wind_dir_meteo = 0
                elif v[t] < 0:
                    wind_dir_meteo = 180
                    
            elif u[t] != 0 and v[t] == 0:
    
                if u[t] > 0:
                    wind_dir_meteo = 270
                elif u[t] < 0:
                    wind_dir_meteo = 90     
                        
            wind_dir_meteo_list.append(wind_dir_meteo)   

    wind_dir_meteo_array = np.array(wind_dir_meteo_list).astype('d')
    
    return wind_dir_meteo_array


def dewpoint_temperature(T, rh):
    
    # Adapted from https://content.meteoblue.com/es/especificaciones/variables-meteorologicas/humedad
    # Uses Magnus´ formula
    
    if not isinstance(T, list):
        T = np.array(T)
         
    if not isinstance(rh, list):
        rh = np.array(rh)

    t_shape = T.shape
    rh_shape = rh.shape
    
    if t_shape != rh_shape:
        raise ValueError("Temperature and relative humidity arrays"
                         "must have the same shape.")
        
    c2p, c2n, c3p, c3n = return_constants()

    Td = T.copy()
    
    T_pos_mask = T>0
    T_neg_mask = T<0
    
    T_pos_masked = T[T_pos_mask]
    T_neg_masked = T[T_neg_mask]
    
    rh_pos_masked = rh[T_pos_mask]
    rh_neg_masked = rh[T_neg_mask]
    
    Td[T_pos_mask]\
    = (np.log(rh_pos_masked/100) + (c2p*T_pos_masked) / (c3p+T_pos_masked))\
      / (c2p - np.log(rh_pos_masked/100) - (c2p*T_pos_masked) / (c3p+T_pos_masked))\
      * c3p
        
    Td[T_neg_mask]\
    = (np.log(rh_neg_masked/100) + (c2n*T_neg_masked) / (c3n+T_neg_masked))\
      / (c2n - np.log(rh_neg_masked/100) - (c2n*T_neg_masked) / (c3n+T_neg_masked))\
      * c3n

    return Td


def relative_humidity(T, Td):
    
    # Adapted from https://content.meteoblue.com/es/especificaciones/variables-meteorologicas/humedad
    # Uses Magnus´ formula
    
    if not isinstance(T, list):
        T = np.array(T)
         
    if not isinstance(Td, list):
        Td = np.array(Td)

    t_shape = T.shape
    td_shape = Td.shape
    
    if t_shape != td_shape:
        raise ValueError("Temperature and relative humidity arrays"
                         "must have the same shape.")

    rh = T.copy()
    
    c2p, c2n, c3p, c3n = return_constants()
    
    T_pos_mask = T>0
    T_neg_mask = T<0
    
    T_pos_masked = T[T_pos_mask]
    T_neg_masked = T[T_neg_mask]
    
    Td_pos_masked = Td[T_pos_mask]
    Td_neg_masked = Td[T_neg_mask]
    
    rh[T_pos_mask] = 100*np.exp(c2p * (T_pos_masked*(c3p - Td_pos_masked)\
                                       +  Td_pos_masked*(c3p+T_pos_masked))\
                                / ((c3p + T_pos_masked)*(c3p + Td_pos_masked)))
        
    rh[T_neg_mask] = 100*np.exp(c2n * (T_neg_masked*(c3n - Td_neg_masked)\
                                       +  Td_neg_masked*(c3n+T_neg_masked))\
                                / ((c3n + T_neg_masked)*(c3n + Td_neg_masked)))

    return rh


def return_constants():
    
    # Adapted from https://content.meteoblue.com/es/especificaciones/variables-meteorologicas/humedad 
    
    # Constants for T > 0:
    c2p = 17.08085,
    c3p = 234.175 
 
    # Constants for T < 0:
    c2n = 17.84362
    c3n = 245.425  
    
    return c2p, c2n, c3p, c3n