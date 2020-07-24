from pymatgen.electronic_structure.plotter import DosPlotter
from numpy import gcd
from getMass import Mass
from nearestNeighbors import nearNeighbors




class Compound:
    '''
    This class is meant to take in a VaspRun object and 
    make it more accessible to get some of its attributes. 
    These attributes are listed below.
    Typical usage looks like::
        
        var = Compound( VaspRun_object )
        compound_mass = var.mass
        plot = var.getPlot()
    
    **Attributes**
    
    .. attribute:: vasp
    
        The vasp object itself
    
    .. attribute:: z (lowercase)
    
        The Z component of the compound.
        i.e. the greatest common
        denominator of the compound.
        
        ex. Ag2Bi2I8 --> AgBiI4 ...... z = 2
        
    .. attribute:: formula
        
        The reduced formula of the compound
        
    .. attribute:: full_formula
    
        The full formula used at the start of the VASP run
        
    .. attribute:: elem_List
    
        A list of all the elements in the compound
        
        ex. Ag2Bi2I8 --> ['Ag', 'Bi', 'I']
        
    .. attribute:: mass
    
        The total mass of the object given in AUs or Daltons
        
    .. attribute:: volume
    
        The volume of the cell containing the compound given in
        Angstroms cubed
        
    .. attribute:: density
    
        The density of the compound. This is multiplied by 1.66054
        to make the units grams/cm^3
        
    .. attribute:: neighbors
    
        A list of each of the atoms nearest neighbors to one another.
        See 
        
    .. attribute:: latConst
    
        A list of the 'a b c' lattice constants in the compound
        
        i.e. [a const, b const, c const]
        
    
    **Methods**
    
    .. method:: getPlot()
        
        Returns a Density of states plot
    
    '''
    def __init__(self, vasp):
        self.vasp = vasp
        self.z = self.getGCD()
        self.formula = self.getElem()
        self.full_formula = self.getElem(False)
        self.elem_List = self.elList()
        self.mass = Mass(vasp.atomic_symbols)
        self.volume = vasp.final_structure.volume
        self.density = self.mass / self.volume * 1.66054
        self.neighbors = nearNeighbors(vasp)
        self.latConst = self.getLatConst()
        
        self.plot = DosPlotter()
    
        
    
    def elList(self):
        lis = []
        temp = {}
        
        for x in self.vasp.atomic_symbols:
            if x in temp:
                temp[x] += 1
            else:
                temp[x] = 1 
                
        for x in temp:
            lis.append(x)
            
        return lis
    
    def getNeighbor(self, el1, el2):
        return self.neighbors[el1 + '-' + el2]
    
    def getGCD(self):
        el = {}
        for x in self.vasp.atomic_symbols:
            if x in el:
                el[x] += 1
            else:
                el[x] = 1
                
        return gcd.reduce([el[x] for x in el])
    
    def getElem(self, pretty=True):
        string = ""        
        el = {}
        for x in self.vasp.atomic_symbols:
            if x in el:
                el[x] += 1
            else:
                el[x] = 1
                
        for x in el:
            if pretty:
                num = int(el[x]/self.z)
            else:
                num = int(el[x])
                
            if num == 1:
                string += x
            else:
                string += x + str(num)
            
        return string
    
    def getPlot(self):
        self.plot.add_dos("Total Dos", self.vasp.complete_dos)
        return self.plot.get_plot()
    
    def getLatConst(self):
        return self.vasp.final_structure.lattice.abc

