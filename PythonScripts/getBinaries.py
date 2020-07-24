'''

For the compounds of interest, we will be looking at the compounds used to 
form them.

The compound structures ABC4 and A3BC6 are formed by the compostions of 
AC+BC3 and 3AC+BC3 respectively.

This script gathers all the compound's composition compounds to study their
formation energies to see if the structure is even feesible to make.

There are multiple instances of these compounds so we will sort them out,
using only the ones with the lowest formation energies

'''


from pymatgen import MPRester
import pickle


#My API key
MAPI_KEY = "q8pQyFEnL5Z7O2oc"

#Elements to get
a = ["Cu", "Ag", "Au"]
b = ["As", "Sb", "Bi"]
c = ["Cl", "Br", "I"]

#Properties to get
prop = ['material_id', 
        'band_gap', 
        'pretty_formula',
        'cif',
        'input.incar',
        'input.kpoints',
        'energy']

mpr = MPRester(MAPI_KEY)  # Object for connecting to MP Rest interface


##############################################################
#Loop to get all AC the elements
resultAC = []
for x in a:
    for y in c:
        resultAC.append(mpr.query(
                    criteria = x+y, 
                    properties= [*prop]))
        
# Gets lowest formation energy
formationAC = []
count = 0
for x in resultAC:
    formationAC.append(x[0])
    for y in x:
        if y['energy'] < formationAC[count]['energy']:
            formationAC[count] = y
    count += 1            



#########################################################       
#Loop to get all BC3 the elements
resultBC = []
for x in b:
    for y in c:
        resultBC.append(mpr.query(
                    criteria = x+y+'3', 
                    properties= [*prop]))
        

# Gets lowest formation energy
formationBC = []
count = 0
for x in resultBC:
    formationBC.append(x[0])
    for y in x:
        if y['energy'] < formationBC[count]['energy']:
            formationBC[count] = y
    count += 1


######################################################

# Creating a dictionary to export for later use
new = {}

# Adds AC compounds
for group in formationAC:
    new[group["pretty_formula"]] = group

# Adds BC3 compounds
for group in formationBC:
    new[group["pretty_formula"]] = group

# Writes dictionary to a file for later use in other programs
pickle.dump( new, open( "Data/diffElements.p", "wb" ) ) 

### End of script