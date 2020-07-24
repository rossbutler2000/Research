'''

This script will take .cif files from compounds of interest and create new 
.cif files replacing elements with elements of interest.

'''


import os
import pickle

# Directory structure names
#
cif_path = "Data/Cifs/" # The head of the *.cif file structure
structure_path = ["ABC4/", "A3BC6/"] # Folders in the form or their structure



# Elements of interest
oldCif = ["AgBiI4", "Ag3BiBr6"]

# Elements to be copied    
a = ["Cu", "Ag", "Au"]
b = ["As", "Sb", "Bi"]
c = ["Cl", "Br", "I"]  

# Constant variables needed to be replaced
formula_marker = "_chemical_formula_sum"

# Elements data
elements = pickle.load( open( "Data/elements.p", "rb" ) )



# Makes file cif_path for new CIF files
try:
    os.mkdir(cif_path)
except FileExistsError:
    0
    
for x in structure_path:
    try:
        os.mkdir(cif_path + x)
    except:
        0
        

    
# Loop to extract and change data
for num in range(len(structure_path)):
    # Get Data
    fdata = elements[oldCif[num]]['cif']
    
    
    # Finding 3 part chemical formula
    start = fdata.find(formula_marker)
    start = fdata.find("'", start)
    stop = fdata.find("'", start+1)
    formula = fdata[start:stop].split()
    simple_formula = []
    for i in range(0,3):
        simple_formula.append(formula[i].strip("'0123456789"))
    # This method will need to change if the variable '_chemical_formula_sum' is not in the .cif file
    
    
  
    # Replacing all instances
    for i in a:
        for j in b:
            for k in c:
                # Raplaces data
                new_data = fdata.replace(simple_formula[0], i)
                new_data = new_data.replace(simple_formula[1], j)
                new_data = new_data.replace(simple_formula[2], k)
                
                # Making file name
                name = formula[0].replace(simple_formula[0], i)
                name += formula[1].replace(simple_formula[1], j)
                name += formula[2].replace(simple_formula[2], k)
                name += ".cif"
                name = name.strip("'")
                
                # Creating and writing to file
                f = open(cif_path+structure_path[num]+name,'w')
                f.write(new_data)
                f.close()
    
# End of script