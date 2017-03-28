import sys
import os
import numpy as np
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
import psdPost
import lfmViz as lfmv

#--------------------------------------------
# parameters
folder = 'C:\\work\\space_weather\\injs\\vdisttest'
outfolder = 'cell1'
h5file = 'p_Cell#1.h5'
varname = 'f'
cblabel = 'Phase Space Density'
steps = np.arange(9,10)
logx = False
logy = False
logval = True
doPlot = True
doSave = False
#--------------------------------------------


h5path = folder + '\\' + h5file
outfolderPath = folder + '\\' + outfolder
if doSave and (not os.path.exists(outfolderPath)):
    os.makedirs(outfolderPath)

globalMin = 1e30
globalMax = -1e30

for i in steps:
    x,y,d = psdPost.getVelDist(h5path,i,varname)
    if logval:
        d[d == 0.0] = 1e-20
    globalMin = min(globalMin, np.min(d))
    globalMax = max(globalMax, np.max(d))

globalMin = 1e-7
# globalMax = 1e-1

for i in steps:
    x,y,d = psdPost.getVelDist(h5path,i,varname)
    if logval:
        d[d == 0.0] = 1e-20

    plt.cla()
    if logval:
        plt.pcolormesh(x, y, d, norm=mpl.colors.LogNorm(vmin=globalMin, vmax=globalMax))
    else:
        plt.pcolormesh(x, y, d, vmin=globalMin, vmax=globalMax)

    if logx:
        plt.xscale('log')
    if logy:
        plt.yscale('log')

    plt.xlabel('Velocity Perpendicular')
    plt.ylabel('Velocity Parallel')

    plt.colorbar(label=cblabel)

    fig = plt.gcf()
    fig.set_size_inches(21, 9, forward=True)

    mpl.rcParams.update({'font.size': 20})

    if doSave:
        plt.savefig(outfolderPath + '\\a' + str(i) + '.png', dpi=100)
    if doPlot:
        plt.show()
