import sys
import os
import numpy as np
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import psdPost

# for Re 6, MLT 20
# from injs folder
# python ..\lfm2box\pylfm\psdCellPlotKHist.py p2\p_Cell#1.h5 O2\O_Cell#1.h5 Hep2\Hep_Cell#1.h5 Hepp2\Hepp_Cell#1.h5

#--------------------------------------------
# parameters
varname = 'I'
cblabel = 'Intensity'
title = 'Intensity by Species\nL = 8, MLT 20:00'
steps = np.arange(0,270)
logval = True
dmin = 5e1
dmax = 5e4
doPlot = True
doSave = False
cmap = 'plasma'
figSize = (10,10)
figQ = 300
#--------------------------------------------

psdfiles = [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]]


fig = plt.figure(figsize=figSize)
H = 15
gs = gridspec.GridSpec(6,1,height_ratios=[H,H,H,H,2,1],hspace=0.2)

species = ['p','O+','He+','He++']
Ns = len(species)
for i in range(Ns):
    s = species[i]

    Ax = fig.add_subplot(gs[i,0])
    x,y,d = psdPost.getCellKHist(psdfiles[i],steps,varname)

    d[d < dmin] = 0.0

    # dmin = np.min(d)
    # dmax = np.max(d)
    # if dmin == 0.0:
    #     dmin = 1e-20

    cnorm = mpl.colors.LogNorm(vmin=dmin,vmax=dmax)
    Ax.pcolormesh(x, y, d, norm=cnorm, cmap=cmap)
    plt.xlim([1800,4450])
    plt.ylim([4,750])

    plt.yscale('log')
    plt.ylabel('keV')

    if i == 3:
        plt.xlabel('time (s)')

    Ax.text(1825,20,species[i],fontsize="large")


Ax = fig.add_subplot(gs[-1,0])
cb1 = mpl.colorbar.ColorbarBase(Ax, cmap=cmap, norm=cnorm, orientation='horizontal', label=cblabel)


plt.suptitle(title)
# mpl.rcParams.update({'font.size': 20})

if doSave:
    plt.savefig('cell_khist_' + varname + '.png', dpi=100)
if doPlot:
    plt.show()
