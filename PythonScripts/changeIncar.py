"""

This script will change data in an INCAR file.

Only changes one value at a time

"""

def incar(string, val):
    # Gets data
    f = open("INCAR")
    fdata = f.read()
    f.close()
    
    # Changes data
    start = fdata.find(string)
    if start > 0:
        end = start + fdata[start:].find('\n')
        line = fdata[start:end].split('=')
        line[1] = str(val)
        line = '= '.join(line)
        fdata = fdata.replace(fdata[start:end], line)
    else:
        fdata += string + " = " + str(val)
        
    f = open("INCAR", 'w')
    f.write(fdata)
    f.close()

# End of script