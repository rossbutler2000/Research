'''

This script is meant to get the total mass of a compound in AUs or Daltons.
Not all masses are listed with the 'mass.dat' file. An error will appear
if an element is passed in that is not in the data file. The user will need
to add the mass to the file in the same style as how all the other masses
are listed.

'''
import os

os.chdir("..")
mass_file = os.path.abspath(os.curdir) + "/Data/elements.dat"

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
        
    **Warning**
    
        An error will occur if the element is not included in the mass.dat
        file. The user will be required to add it to the file in the same 
        fasion as the others are in. i.e.::
            
            # First the element, a space, then its mass in AU
            I 126.90447
            Sb 121.76
            
            # Do not get rid or replace the first line
            # Order of elements does not matter
    '''
    
    m = 0.0
    for x in lis:
        try:
            m += masses[x]
        except KeyError:
            raise KeyError(r"Data/mass.dat does not have information on the\
                           element " +"'"+x+"'.\nYou must add it to the\
                           data file.\n(See documentation for details)")
        
    return m

