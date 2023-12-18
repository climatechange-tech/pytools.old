#-------------------------#
# Define custom functions #
#-------------------------#

def cat(fitxategia):
    
    """
    Prints the content of a file specified in an absolute or relative path
    the same way as it does the ´cat´ UNIX command.
    
    Parameters
    ----------
    path : str or PosixPath
          Absolute or relative path
          
    Returns
    -------
    The path is always case-sensitive.
    If the path exists, it returns the string of the whole content
    of the specified path, else throws a FileNotFoundError.
    """
    
    try:
        file = open(path)
        
        for line in file:
            line_no_extra_whitespaces = line.strip()
            print(line_no_extra_whitespaces)
        file.close()
        
    except FileNotFoundError():
        print("No such file or directory. "
              "Try fixing misspellings or check path's components.")
        
        
#-------------------#
# Call the function #
#-------------------#
        
path = input('Enter the path to the file to be read: ')
cat(path)

