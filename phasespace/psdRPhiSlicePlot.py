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
folder = 'C:\\work\\space_weather\\test_data'
psdfile = 'psd_r_phi_Slice2D#1.h5'
slicename = 'r_phi'
varname = 'I'
cblabel = 'Intensity'
n = np.arange(0,3)
flipaxes = False
logx = False
logy = False
logval = True
doPlot = True
doSave = False
#--------------------------------------------


# https://github.com/ksorat/Magnetoloss/blob/master/panels/fpPanel.py
def getFld(vtiDir,t,dt=10.0,eqStub="eqSlc"):
	tSlc = np.int(t/dt)
	vtiFile = vtiDir + "/" + eqStub + ".%04d.vti"%(tSlc)

	dBz = lfmv.getVTI_SlcSclr(vtiFile).T
	ori,dx,ex = lfmv.getVTI_Eq(vtiFile)
	xi = ori[0] + np.arange(ex[0],ex[1]+1)*dx[0]
	yi = ori[1] + np.arange(ex[2],ex[3]+1)*dx[1]

	return xi,yi,dBz



psdpath = folder + '\\' + psdfile
outfolder = folder + '\\' + slicename

if doSave and (not os.path.exists(outfolder)):
    os.makedirs(outfolder)

globalMin = 1e30
globalMax = -1e30

isFirst = True
for i in n:
    x,y,d = psdPost.getSliceData(psdpath,i,slicename,varname,flipaxes)
    if logval:
        d[d == 0.0] = 1e-20
    globalMin = min(globalMin, np.min(d))
    globalMax = max(globalMax, np.max(d))

globalMin = 1e-8
# globalMax = 1e-1


xi,yi,dBz = getFld('C:/work/space_weather/test_data/LFMDataEqSlcs', 8, dt=1)


for i in n:
    x,y,d = psdPost.getSliceData(psdpath,i,slicename,varname,flipaxes)
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

    plt.xlabel('x (Re)')
    plt.ylabel('y (Re)')

    def fmt(x,pos):
        a, b = '{:.2e}'.format(x).split('e')
        b = int(b)
        return r'${} \times 10^{{{}}}$'.format(a, b)
    # if isFirst:
        #plt.colorbar(format=mpl.ticker.FuncFormatter(fmt))
    plt.colorbar(label=cblabel)
        # isFirst = False

    mpl.rcParams['contour.negative_linestyle'] = 'solid'
    cs = plt.contour(xi,yi,dBz, cmap=plt.get_cmap('Blues')) #colors='w')
    # cs = plt.contourf(xi,yi,dBz, alpha=0.35, cmap=plt.get_cmap('binary'))

    fig = plt.gcf()
    fig.set_size_inches(15, 12, forward=True)

    mpl.rcParams.update({'font.size': 20})

    if doSave:
        plt.savefig(outfolder + '\\a' + str(i) + '.png', dpi=100)
    if doPlot:
        plt.show()
