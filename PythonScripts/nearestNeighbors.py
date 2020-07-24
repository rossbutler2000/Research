'''

This script is meant to find the nearest neighbors of each atom
to each other atom. The user is really only meant to use the 
nearNeighbors function to find these values. 

'''

from numpy import sqrt



# Assigns atoms in respective coordinate to supercell
def superCoords(lat):
	'''
	This function creates a supercell around the cell.
	Not intended for the users use.
	'''
	latM = [ lat['lattice']['matrix'][0], lat['lattice']['matrix'][1],
			lat['lattice']['matrix'][2] ]
	
    # Unit Coordinates
	coords = []
	for x in lat['sites']:
		coords.append([x["species"][0]["element"], x["abc"]])
        
    
	sc = {}
	for c in coords:
		atoms = []
		for x in range(-1, 2):
			for y in range(-1, 2):
				for z in range(-1, 2):
					if x != 0 or y != 0 or z !=0:
						atoms.append([(c[1][0]+x)*latM[0][0]+(c[1][1]+y)*latM[1][0]+(c[1][2]+z)*latM[2][0], 
                                      (c[1][0]+x)*latM[0][1]+(c[1][1]+y)*latM[1][1]+(c[1][2]+z)*latM[2][1], 
                                      (c[1][0]+x)*latM[0][2]+(c[1][1]+y)*latM[1][2]+(c[1][2]+z)*latM[2][2]])
		if c[0] in sc:
			sc[c[0]].append(atoms)
		else:
			sc[c[0]] = [atoms]
        
	return sc


# Distance formula                    
def dist(ar1, ar2):
	'''
	A function that measures the distance between 2 points.
	'''
	result = 0
    
	for i in range(3):
		result += (ar1[i]-ar2[i])**2
        
	return sqrt(result)


def nearNeighbors(vrun):
	'''
	This function takes in a VaspRun object and outputs a dictionary of 
	the nearest neighbors of each atom to each other atom.::
		
		var = nearNeighbors(VaspRun_object)
		# var == [[neighbor 1: length], [neighbor 2: length], ... ]
	'''
	
	result = {}
	lat = vrun.final_structure.as_dict()
    
	sCoords = superCoords(lat)
    
    # Listing of the elements
	elem = []
	for el in lat['sites']:
		elem.append(el['species'][0]['element'])
    
    # Gets nearest neighbors within cell
	for a1 in range(len(lat['sites'])):
		for a2 in range(len(lat['sites'])):
			if a1 != a2 and a1 < a2:
				combo = elem[a1] + '-' + elem[a2]
				numb = dist(lat['sites'][a1]['xyz'], lat['sites'][a2]['xyz'])
				if combo in result:
					if numb < result[combo]:
						result[combo] = numb
				else:
					result[combo] = numb
        
    # Gets nearest neighbors of atoms in cell to super cell
	for a1 in range(len(lat['sites'])):
		for key in sCoords:
			for lis in sCoords[key]:
				combo = ''
				if key + '-' + elem[a1] in result:
					combo = key + '-' + elem[a1]
				else:
					combo = elem[a1] + '-' + key
				for a2 in lis:
					numb = dist(lat['sites'][a1]['xyz'], a2)
					if combo in result:
						if numb < result[combo]:
							result[combo] = numb
					else:
						result[combo] = numb
                      
	return result
    