#----------------#
# Import modules #
#----------------#

import piso
piso.register_accessors()

#------------------#
# Define functions #
#------------------#

def basic_interval_operator(interval_array,
                            operation="union", 
                            force_union=False):

    # TODO: diseinatu pd.arrays.IntervalArray motako matrizea, "interval_array" zerrenda edo numpy matrize bat izanik
    
    # Ideia orokorra mantentzeko, laneko programa nagusitik hartutako zatia #
    
    # intervals = pd.arrays.IntervalArray(df_slice_bins,
    #                                     closed="left")
    
    # min_num_interval = intervals.min()
    # min_num_interval_left = min_num_interval.left
    
    # max_num_interval = intervals.max()
    # max_num_interval_right = max_num_interval.right
    
    # merged_bin = intervals.piso.union()[0]
    # merged_bin_left = merged_bin.left
    # merged_bin_right = merged_bin.right
    
    # if merged_bin_left != min_num_interval_left\
    #     or merged_bin_right != max_num_interval_right:
    #         merged_bin = pd.Interval(min_num_interval_left,
    #                                  max_num_interval_right,
    #                                  closed="left")
    
# def define_interval(method="pandas | intervaltree", closed="both"):
    
