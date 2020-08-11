#!/bin/bash


# Loads up Pymatgen and other dependencies
# User may need to change depending on their setup
module load python/3.6.3-anaconda5.0.1
source activate pymatgen

# Pathing variables
py=PythonScripts/
dat=Data/

# Creates CIF files which will be used to create individual POSCARs
python ${py}createCIF.py

# Creates all file structure with files included
python ${py}input.py