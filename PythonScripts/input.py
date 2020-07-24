'''

This script is meant to create a file structure in which vasp runs will be
conducted

It will create a folder for each compound of interest

In each folder it will place the files KPOINT, INCAR, *.cif, POTCAR, and run
into each respective directory

It will also create a POSCAR file out of the *.cif file provided

'''


import pickle
import os
import shutil

from cif2Pos import c2p
from createPotcar import pot
from util import move_file
from changeIncar import incar


# Directory structure names
#
main_path = "VaspRuns/" # Path where all files will be found
data_path = "Data/"
cif_path = data_path + "Cifs/" # Path where CIF files are found

cif = os.listdir(cif_path) # Cifs folder contents


# Folders in the form or their structure
structure_path = ["ABC4/", "A3BC6/"]

# Elements of interest
eoi = ["AgBiI4", "Ag3BiBr6", [],]

# Elements found
elements = pickle.load( open( "Data/elements.p", "rb" ) )


# Creates folder where the vasp runs will take place
try:
    os.mkdir(main_path)
except FileExistsError:
    0



# Creates file structure  
for num in range(len(structure_path)):
    input_path = main_path + structure_path[num]
    try:
        os.mkdir(input_path)
    except FileExistsError:
        0
    
    compounds = os.listdir(cif_path+structure_path[num])
    for files in compounds:
        # Creates path directory
        try:
            os.mkdir(input_path+'/'+files[:-4]+'/')
        except FileExistsError:
            0
        
        
        # Gets chemical formula
        num_formula = files[:-4]
        
        
        # Folder where files will be found
        path = input_path+num_formula+'/runnable'
        try:
            os.mkdir(path)
        except:
            0
        
        # Makes POTCAR and moves it
        pot(files)
        move_file("POTCAR", path)
        
        # Puts CIF file in directory
        shutil.copy(cif_path+structure_path[num]+files, path)
        
        # Creates POSCAR file and moves it
        c2p(cif_path+structure_path[num]+files)
        move_file("POSCAR", path)
        
        # INCAR
        elements[eoi[num]]["input.incar"].write_file("INCAR")
        incar("NSW", 100)
        incar("NPAR", 10)
        move_file("INCAR", path)
        
        # KPOINTS
        elements[eoi[num]]["input.kpoints"].write_file("KPOINTS")
        move_file("KPOINTS", path)
        
        # run
        shutil.copy("Data/run", path)
        
#### End of script