'''

This script contains a function which creates POTCAR files for compounds

It gets data from single element POTCAR files and concatinates them into
larger POTCAR files for the entire compound

'''

import os

data_path = "Data/"
potcar_path = data_path + "Potcars/" # Path where POTCAR files are found
potcar = os.listdir(potcar_path) # Potcas folder contents


def pot(cif):
    # Gets chemical formula
    simple_formula = cif[:-4]
    for i in range(0,10):
        simple_formula = simple_formula.replace(str(i), ' ')
    for i in range(len(simple_formula)):
        if simple_formula[i].islower():
            simple_formula = simple_formula.replace(simple_formula[i], 
                                                    simple_formula[i]+' ')
        # if simple_formula[i].islower():
        #     if 
    simple_formula = simple_formula.split()
    
    
    # Creates POTCAR file
    data = ''
    for element in simple_formula:
        # Gets POTCAR data
        file = open(potcar_path+element+'/POTCAR')
        data += file.read()
        file.close()
    
    # Puts fileCAR file into directory    
    file = open('POTCAR', 'w')
    file.write(data)
    file.close()
    
# End of script