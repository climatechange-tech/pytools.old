#----------------#
# Import modules #
#----------------#

import os

#------------------#
# Define functions #
#------------------#

def exec_shell_command(command_str):
    os.system(command_str)
    
def catch_shell_prompt_output(command_str):
    output_str = os.popen(command_str).read()
    return output_str
