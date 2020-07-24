'''

Contains function 'c2p' which makes a .cif file into a POSCAR file

'''

import numpy as np
from util import parsefor


# Constant variables
symb = '_atom_site_type_symbol'
x = '_atom_site_fract_x'
y = '_atom_site_fract_y'
z = '_atom_site_fract_z'



  

# Converts .cif to .vasp
def c2p(cif):
    # Getting data from files
    file = open(cif, 'r')
    fdata = file.read()
    file.close()
    
    
    # Seperating data (a, b, c, alpha, beta, gamma)
    a = parsefor(fdata, '_cell_length_a')
    b = parsefor(fdata, '_cell_length_b')
    c = parsefor(fdata, '_cell_length_c')
    alpha = np.radians(parsefor(fdata, '_cell_angle_alpha'))
    beta = np.radians(parsefor(fdata, '_cell_angle_beta'))
    gamma = np.radians(parsefor(fdata, '_cell_angle_gamma'))
    
    # Creating unit cell
    unit_cell = [[a, 0, 0]]
    unit_cell.append([b*np.cos(gamma), b*np.sin(gamma), 0])
    
    tVal1 = c*np.cos(beta)
    tVal2 = (c*(np.cos(alpha)-(np.cos(gamma)*np.cos(beta))))/np.sin(gamma)
    unit_cell.append([tVal1, tVal2, np.sqrt(c**2-tVal1**2-tVal2**2)])
    
    # Seperates coordinates
    atm = '_atom_site_'
    oStart = fdata.find(atm)
    arrayNum = fdata.count(atm)
    oEnd = 0
    
    label = []
    for i in range(0, arrayNum):
        oEnd = fdata.find('\n', oStart)
        label.append(fdata[oStart:oEnd].lstrip())
        oStart = oEnd + 1
    
    coord ={}
    while oStart < len(fdata):
        if fdata[oEnd+1] == '\n':
            break
        oEnd = fdata.find('\n', oStart)
        temp = fdata[oStart:oEnd].split()
       
        if temp[label.index(symb)] not in coord:
           coord[temp[label.index(symb)]] = [[temp[label.index(x)], temp[label.index(y)], temp[label.index(z)]]]
        else:
           coord[temp[label.index(symb)]].append([temp[label.index(x)], temp[label.index(y)], temp[label.index(z)]])
           
        oStart = oEnd + 1
       
    # Creates POSCAR string
    vasp_string = "COMMENT\n1.00000000000000\n"
    for i in range(0,3):
        for j in range(0,3):
            if j < 2:
                vasp_string += str(unit_cell[i][j]) + ' '
            else:
                vasp_string += str(unit_cell[i][j]) + '\n'
                
    for i in coord:
        vasp_string += i + " "
    vasp_string += '\n'
    
    for i in coord:
        vasp_string += str(len(coord[i])) + ' '
    vasp_string += '\nDirect\n'
    
    for i in coord:
        for j in range(0, len(coord[i])):
            for k in range(0, 3):
                vasp_string += str(coord[i][j][k]) + ' '
            vasp_string += '\n'
            
    for i in coord:
        for j in coord[i]:
            vasp_string += "\n0.00000000E+00 0.00000000E+00 0.00000000E+00"
    
    name = ''
    for i in coord:
        if len(i) > 1:
            name += i + str(len(i))
        else:
            name += i
    
    
    # Writes to POSCAR file
    new_file = open("POSCAR", 'w')
    new_file.write(vasp_string)
    new_file.close()
    
################### End of script