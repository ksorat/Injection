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
usebnds = True
title = 'Equatorial Slice'
tmpvid = 'tmpVid1'

varNames = ['f', 'I', 'AvgK', 'Ntp']
varTitles = ['Phase Space Density', 'Intensity', 'Average Energy', '# Test Particles']
varBnds = [ [1e-9,1e-5], [1e-1,1e2], [0.0,650.0], [1.0,1000.0] ]
bnds = varBnds[vi]

# legends
plXs = [0.03]
plYs = [0.0, 0.0, 0.9, 0.55]
plTits = ["", "", varTitles[vi]]

# dbs[0] = hemisphere1.stl file
# dbs[1] = hemisphere2.stl file
# dbs[2] = r/phi xmf file
#[dbs[3] = magnetic field slices]
sphereDir = os.path.dirname(os.path.realpath(__file__))
dbs = [sphereDir + '/hemisphere1.stl', sphereDir + '/hemisphere2.stl', sys.argv[1]]
if len(sys.argv) > 2:
    dbs.append(sys.argv[2] + "/eqSlc.*.vti database")
    plTits.append("B Mag")
    plotB = True
else:
    plTits.append("")
    plotB = False

AddArgument("-nowin")
Launch()
for db in dbs:
    print "Opening Database: " + db
    OpenDatabase(db)
CreateDatabaseCorrelation("c", dbs, 0)

pyv.lfmExprs()

pyv.plotMesh(dbs[0], 'STL_mesh', meshColor=(240,240,240,255), opaqueColor=(240,240,240,255), Legend=False)
pyv.plotMesh(dbs[1], 'STL_mesh', meshColor=(0,0,0,255), opaqueColor=(0,0,0,255), Legend=False)

if usebnds:
    pyv.lfmPCol(dbs[2], varNames[vi], vBds=bnds, Log=True, cMap='plasma')
else:
    pyv.lfmPCol(dbs[2], varNames[vi], Log=False, cMap='plasma')
pyv.addThreshold(varNames[vi], bnds[0], 1e10)

if plotB:
    pyv.plotContour(dbs[3], 'Bmag', cmap='viridis', values=(10,20,30,40,50,60,70,80), Legend=True, lineWidth=0, lineStyle='solid')
    # pyv.plotContour(dbs[3], 'Bz', cmap='RdYlBu', values=(-30,-20,-10,0,10,20,30), Legend=True, lineWidth=0, lineStyle='solid')
    pyv.to3D()

pyv.genPolarCoords(dbs[2], 2, 10, 45)
pyv.genMarkerXY(6.0, 90.0, 120.0, 0.5, color=(173,27,27,255), lineWidth=2)

speciesStr = "Species: " + species
pyv.genTit( titS=speciesStr, Pos=(0.7,0.87), height=0.02 )
pyv.genTit( titS="Energies: All", Pos=(0.7,0.91), height=0.02 )
tit = pyv.genTit( titS=title, Pos=(0.35,0.955), height=0.03 )
pyv.cleanLegends(plXs,plYs,plTits, plHt=0.015)
pyv.setAtts(pWidth=1000, VidDir=tmpvid)

DrawPlots()

md = GetMetaData(dbs[2])
dt = md.times[1] - md.times[0]
pyv.doTimeLoop(Ninit=0, Nfin=1, T0=T0, dt=dt, Save=True, tLabPos=(0.35,0.05) )

outVid = "vid_r_phi_" + varNames[vi] + "_all.mp4"
pyv.makeVid(outVid=outVid, vidDir=tmpvid, overwrite=True)