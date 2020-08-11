from pymatgen.io.vasp import Vasprun
from matplotlib import pyplot as plt
from Compound import Compound
import os



elelist = {}
count = 1
for x in open("ele.txt").readlines():
    temp = x.split("-")
    elelist[temp[0].strip()] = count
    count += 1

def get_value(el):
    return elelist[el]


class MultiPlot:
    
    def __init__(self, comps, row=15, col=15):
        self.row = row
        self.col = col
        self.fig = plt.figure(figsize=(self.col, self.row))
        self.figXLabel = None
        self.figYLabel = None
        self.comps = comps
        self.axes = []
        self.order = [9, 3, 1]
    
    # def 
    
    def add_plot(self, plot):
        self.plots.append(plot)
        
    def plot(self, *args, **kwargs):
        for i in range(len(self.comps)):
            dat = self.comps[i].getPlot().gca().figure.axes[0]
            self.axes.append([self.fig.add_subplot(*self.order), dat.properties()])
            self.axes[i][0].plot(*dat.lines[0].get_data(), *args, **kwargs)
            self.axes[i][0].text(0.75, 0.75, self.comps[i].formula,
                              transform=self.axes[i][0].transAxes)
            self.axes[i][0].locator_params(tight=True, nbins=5)
            self.order[2] += 1
        self.figYLabel = self.fig.text(0.05, 0.5, self.axes[0][1]['ylabel'] + ' (states/eV)',
                                       rotation="vertical", ha="center", 
                                       va="center", fontsize=20)
        self.figXLabel = self.fig.text(0.5, 0.05, self.axes[0][1]['xlabel'],
                                       ha="center", va="center", fontsize=20)
        
        for i in range(0, len(self.axes)-3):
            self.axes[i][0].xaxis.set_visible(False)
            self.axes[i][0].xaxis.set_ticklabels([])
            
        self.fig.tight_layout(rect=(.07, .07, 1, 1))
        
    def change_fig_size(self, width=None, height=None):
        if width != None:
            self.fig.set_figwidth(width)
        if height != None:
            self.fig.set_figheight(height)
            
    def change_limits(self, xlim=None, ylim=None):
        if xlim != None:
            for ax in self.axes:
                ax[0].set_xlim(*xlim)
        if ylim != None:
            for ax in self.axes:
                ax[0].set_ylim(*ylim)
                
    def save_fig(self, name):
        self.fig.savefig(name)
        
        
    def sort(self):
        lists = {}
        
        for x in self.comps:
            if x.elemList[0] in lists:
                lists[x.elemList[0]].append(x)
            else:
                lists[x.elemList[0]] = [x]
                
        for x in lists:
            tempList = []
            for item in lists[x]:
                check = True
                if not tempList:
                    tempList.append(item)
                    check = False 
                else:
                    for y in range(len(tempList)):
                        if elelist[item.elemList[1]] <= elelist[tempList[y].elemList[1]]:
                            if elelist[item.elemList[2]] < elelist[tempList[y].elemList[2]]:
                                tempList.insert(y, item)
                                check = False
                                break
                            
                if check:
                    tempList.append(item)
                        
            lists[x] = tempList
            
        newList = []
        keys = list(lists.keys())
        keys.sort(key=get_value)
        for i in range(9):
            for j in keys:
                newList.append(lists[j][i])
            
        self.comps = newList


######################################
######################################
######################################



path = "Tuttle/VaspRuns/ABC4/"
xml = "vasprun.xml"

comp = []

for x, q, u in os.walk(path):
    if x.find("runnable") > 0:
        c = Vasprun(x+'/'+xml)
        comp.append(Compound(c))
            

mplot = MultiPlot(comp)
mplot.sort()
mplot.plot(color='r')
mplot.change_limits(xlim=(-15, 10), ylim=(0,20))

mplot.fig.savefig("a3bc6.png")




