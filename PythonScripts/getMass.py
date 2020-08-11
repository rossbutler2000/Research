'''

This script is meant to get the total mass of a compound in AUs or Daltons.
All elements are in order and can also be used to know the order of the
elements.

'''
import os

# Pathing
path = os.path.abspath(os.curdir)
os.chdir("..")
mass_file = os.path.abspath(os.curdir) + "/Data/elements.dat"
os.chdir(path)

# Dictionary of known masses from mass.dat
masses = {}
f = open(mass_file)
f.readline()
for line in f:
    lis = line.split('-')
    for i in range(len(lis)):
        lis[i] = lis[i].strip('\n, ')
    masses[lis[0]] = float(lis[2])
f.close()

def Mass(lis):
    '''
    Returns the total mass of the list of elements.::
        
        
        mass = Mass(['Ag', 'Bi', 'I', 'I'])
        # mass == 570.65754
    '''
	
    if type(lis) != list:
        raise TypeError("The argument of the function must be a Python list.")
	
    
    m = 0.0
    for x in lis:
        try:
            m += masses[x]
        except KeyError:
            raise KeyError("'"+x+"'" + " is not a valid element.")
        
    return m

# End of script