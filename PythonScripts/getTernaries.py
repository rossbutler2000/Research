'''

This script is meant to get the properties of the desired elements in groups 
A, B, and C listed below
See # Elements to get

The desired properties are listed below
see "# Properties to get"
  
After all properties are retrieved, they are stored in a dictionary file using
the 'pickle' library for later use in other programs

'''

from pymatgen import MPRester
import pickle


# My API key
MAPI_KEY = "q8pQyFEnL5Z7O2oc"

# Elements to get
a = ["Cu", "Ag", "Au"]
b = ["As", "Sb", "Bi"]
c = ["Cl", "Br", "I"]

# Properties to get
prop = ['material_id', 
        'band_gap', 
        'pretty_formula',
        'input.incar',
        'input.kpoints',
        'cif',
        'energy']

mpr = MPRester(MAPI_KEY)  # object for connecting to MP Rest interface


# Loop to get all the elements
result = []
load = 27
print("First load: ", load)
for x in a:
    for y in b:
        for z in c:
            result.append(mpr.query(
                    criteria = {"elements":{"$all":[x, y, z]}}, 
                    properties= [*prop]))
            load = load - 1
            print(load)
            
# New dictionary for printing
new = {}
for group in result:
    for x in group:
        new[x["pretty_formula"]] = x
    


# Writes dictionary to a file for later use in other programs
pickle.dump( new, open( "Data/elements.p", "wb" ) )       

### End of script