import sys
import os
import datetime
from visit import *
from visit_utils import *
from visit_utils.common import lsearch
import pyVisit as pyv

species = 'p'
vi = 1
T0 = 0.0
title = 'Meridional Slice'
rotz = 90
tmpvid = 'tmpVid1'

varNames = ['f', 'I', 'AvgK', 'Ntp']
varTitles = ['Phase Space Density', 'Intensity', 'Average Energy', '# Test Particles']
varBnds = [ [1e-9,1e-5], [1e-7, 1e-3], [0.0,650.0], [1.0,1000.0] ]
bnds = varBnds[vi]

# legends
plXs = [0.03]
plYs = [0.0,0.0,0.9,0.9,0.55]
plTits = ["", "", varTitles[vi], varTitles[vi]]

# dbs[0] = hemisphere1.stl file
# dbs[1] = hemisphere2.stl file
# dbs[2] = first r/theta xmf file
# dbs[3] = second r/theta xmf file
#[dbs[4] = magnetic field slices]
sphereDir = os.path.dirname(os.path.realpath(__file__))
dbs = [sphereDir + '/hemisphere1.stl', sphereDir + '/hemisphere2.stl', sys.argv[1], sys.argv[2]]
if len(sys.argv) > 3:
    dbs.append(sys.argv[3] + "/merid90Slc.*.vti database")
    plTits.append("B Curl Norm")
    plotB = True
else:
    plTits.append("")
    plotB = False

AddArgument("-nowin")
Launch()
for db in dbs:
    OpenDatabase(db)
CreateDatabaseCorrelation("c",dbs,0)

pyv.lfmExprs()

pyv.plotMesh(dbs[0], 'STL_mesh', meshColor=(240,240,240,255), opaqueColor=(240,240,240,255))
pyv.plotMesh(dbs[1], 'STL_mesh', meshColor=(0,0,0,255), opaqueColor=(0,0,0,255))

pyv.lfmPCol(dbs[2], varNames[vi], vBds=bnds, Log=True, cMap='plasma', Legend=True)
pyv.addThreshold(varNames[vi], bnds[0], 1e10)
pyv.lfmPCol(dbs[3], varNames[vi], vBds=bnds, Log=True, cMap='plasma', Legend=False)
pyv.addThreshold(varNames[vi], bnds[0], 1e10)

if plotB:
    pyv.plotContour(dbs[4], 'BCurlMagNorm', cmap='viridis', values=(0,0.25,0.5,0.75,1.0), Legend=True, lineWidth=1, lineStyle='solid')
    pyv.addThreshold('RadAll', 2.1, 1e10)
    pyv.addSlice(originType="Percent", percent=50, axis="Y", project2d=False, opNum=1)

pyv.SetWin3D(Ax=0,Ang=-90,Zoom=1.0)
pyv.SetWin3D(Ax=1,Ang=rotz,Zoom=1.0)

pyv.genPolarCoords(dbs[2], 2, 10, 45, aType='theta', phi=90)
pyv.genPolarCoords(dbs[3], 2, 10, 45, aType='theta', phi=270)

phistr = "Phi: " + str(rotz)
pyv.genTit( titS=phistr, Pos=(0.7,0.83), height=0.02 )
speciesStr = "Species: " + species
pyv.genTit( titS=speciesStr, Pos=(0.7,0.86), height=0.02 )
pyv.genTit( titS="Energies: All", Pos=(0.7,0.89), height=0.02 )
tit = pyv.genTit( titS=title, Pos=(0.35,0.955), height=0.03 )
pyv.cleanLegends(plXs,plYs,plTits, plHt=0.015)
pyv.setAtts(pWidth=1000, VidDir=tmpvid)

DrawPlots()

md = GetMetaData(dbs[2])
dt = md.times[1] - md.times[0]
pyv.doTimeLoop(Ninit=250, Nfin=251, T0=T0, dt=dt, Save=True, tLabPos=(0.35,0.05) )

outVid = "vid_r_theta_" + varNames[vi] + "_all.mp4"
pyv.makeVid(outVid=outVid, vidDir=tmpvid, overwrite=True)