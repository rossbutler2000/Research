"""

This script contains several small utility functions which are
used in the various other scripts in this directory.

"""

import os
import shutil


# Move function, deals with files already existing
def move_file(src, dst):
    try:
        shutil.move(src, dst)
    except OSError:
        os.remove(dst+src)
        shutil.move(src, dst)


# Finds values for a, b, c, alpha, beta, gamma
def parsefor(string, value, delim='\n'):
    start = string.find(value) + len(value)
    end = string.find(delim, start)
    
    return float(string[start:end].strip())