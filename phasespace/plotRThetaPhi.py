import sys
import os
import datetime
from visit import *
from visit_utils import *
from visit_utils.common import lsearch
import pyVisit as pyv

species = 'p'
vi = 0
T0 = 0.0
title = 'R Theta Phi Slice'
tmpvid = 'tmpVid1'
plotType = 'contour'

varNames = ['f', 'I', 'AvgK', 'Ntp']
varTitles = ['Phase Space Density', 'Intensity', 'Average Energy', '# Test Particles']
varBnds = [ [1e-14,1e-4], [1e-4,1e5], [0.0,650.0], [1.0,1000.0] ]
bnds = varBnds[vi]

# legends
plXs = [0.03]
plYs = [0.9]
plTits = ["", "", varTitles[vi]]

# dbs[0] = hemisphere1.stl file
# dbs[1] = hemisphere2.stl file
# dbs[2] = r/theta/phi xmf file
sphereDir = os.path.dirname(os.path.realpath(__file__))
dbs = [sphereDir + '/hemisphere1.stl', sphereDir + '/hemisphere2.stl', sys.argv[1]]

AddArgument("-nowin")
Launch()
for db in dbs:
    OpenDatabase(db)
CreateDatabaseCorrelation("c",dbs,0)

pyv.plotMesh(dbs[0], 'STL_mesh', meshColor=(240,240,240,255), opaqueColor=(240,240,240,255), Legend=False)
pyv.plotMesh(dbs[1], 'STL_mesh', meshColor=(0,0,0,255), opaqueColor=(0,0,0,255), Legend=False)

if plotType == 'volume':
    pyv.plotVol(dbs[2], varNames[vi], vBds=bnds, Log=True, Ns=5e6, cmap='plasma')
elif plotType == 'contour':
    colors = [
        (212, 212, 212, 10),
        (162, 181, 209, 20),
        (109, 177, 213, 30),
        (57, 137, 206, 40),
        (9, 119, 222, 50)
    ]
    pyv.plotContour(dbs[2], varNames[vi], vBds=bnds, Log=True, multicolors=colors)

v = GetView3D()
print v
# v.viewNormal = (0.7163064763298141, -0.5781739693301684, 0.3906659610933143)
# v.viewUp = (-0.2785721626199754, 0.2763677136704989, 0.9197926054572146)
# v.viewNormal = (0.6720123069066908, 0.6150760969424318, 0.41240860119063)
# v.viewUp = (-0.2863216028606097, -0.2977870542951664, 0.9106826066361096)
# v.viewNormal = (-0.487723314921487, 0.7350463831844278, 0.4709912766171869)
# v.viewUp = (0.2828575886014731, -0.3773515064105291, 0.8818148474482975)
# v.viewNormal = (-0.7392846217267587, -0.5438270300292107, 0.3971276992202025)
# v.viewUp = (0.3130819684718471, 0.2445421036153976, 0.9177030241734793)
v.viewNormal = (0.01488853966675495, -0.8035801569922378, 0.5950103046796096)
v.viewUp = (0.08057898655461086, 0.5941050518354329, 0.8003413111350991)
v.imageZoom = 1.7
v.SetFocus(0.0, 12.0, 0.0)
SetView3D(v)

speciesStr = "Species: " + species
pyv.genTit( titS=speciesStr, Pos=(0.7,0.87), height=0.02 )
pyv.genTit( titS="Energies: All", Pos=(0.7,0.91), height=0.02 )
tit = pyv.genTit( titS=title, Pos=(0.3,0.955) )
pyv.cleanLegends(plXs,plYs,plTits, plHt=0.015)
pyv.setAtts(pWidth=1000, VidDir=tmpvid)

DrawPlots()

md = GetMetaData(dbs[2])
dt = md.times[1] - md.times[0]
pyv.doTimeLoop(Ninit=0, Nfin=None, T0=T0, dt=dt, Save=True, tLabPos=(0.35,0.05) )

outVid = "vid_r_theta_phi_" + varNames[vi] + "_all.mp4"
pyv.makeVid(outVid=outVid, vidDir=tmpvid, overwrite=True)