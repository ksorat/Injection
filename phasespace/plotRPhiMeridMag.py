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
title = 'Equatorial Slice w/ B Field'
tmpvid = 'tmpVid1'

varNames = ['f', 'I', 'AvgK', 'Ntp']
varTitles = ['Phase Space Density', 'Intensity', 'Average Energy', '# Test Particles']
varBnds = [ [1e-9,1e-5], [1e-7, 1e0], [0.0,650.0], [1.0,1000.0] ]
bnds = varBnds[vi]

# legends
plXs = [0.03]
plYs = [0.0,0.0,0.9,0.55]
plTits = ["", "", varTitles[vi], "B Curl Norm", ""]

# dbs[0] = hemisphere1.stl file
# dbs[1] = hemisphere2.stl file
# dbs[2] = r/phi xmf file
# dbs[3] = magnetic field data slice
sphereDir = os.path.dirname(os.path.realpath(__file__))
dbs = [sphereDir + '/hemisphere1.stl', sphereDir + '/hemisphere2.stl', sys.argv[1], sys.argv[2] + "/merid90Slc.*.vti database"]

AddArgument("-nowin")
Launch()
for db in dbs:
    OpenDatabase(db)
CreateDatabaseCorrelation("c",dbs,0)

pyv.lfmExprs()

pyv.plotMesh(dbs[0], 'STL_mesh', meshColor=(240,240,240,255), opaqueColor=(240,240,240,255))
pyv.plotMesh(dbs[1], 'STL_mesh', meshColor=(0,0,0,255), opaqueColor=(0,0,0,255))

pyv.lfmPCol(dbs[2], varNames[vi], vBds=bnds, Log=True, cMap='plasma', Light=True, Legend=True)
pyv.addThreshold(varNames[vi], bnds[0], 1e10)
pyv.addThreshold("Phi", 90, 270, opNum=1)

pyv.lfmPCol(dbs[3], "BCurlMagNorm", vBds=[0,1], Log=False, cMap='viridis', Light=True, Legend=True)
pyv.addThreshold('RadAll', 2.1, 1e10)
pyv.addSlice(originType="Percent", percent=50, axis="X", project2d=False, opNum=1)

v = GetView3D()
# v.viewNormal = (0.7163064763298141, -0.5781739693301684, 0.3906659610933143)
# v.viewUp = (-0.2785721626199754, 0.2763677136704989, 0.9197926054572146)
# v.viewNormal = (0.6720123069066908, 0.6150760969424318, 0.41240860119063)
# v.viewUp = (-0.2863216028606097, -0.2977870542951664, 0.9106826066361096)
v.viewNormal = (-0.7060372559854389, 0.4591907031665334, 0.5391245600841951)
v.viewUp = (0.45071120230944, -0.295834995183637, 0.8422238821937293)
# v.viewNormal = (-0.7392846217267587, -0.5438270300292107, 0.3971276992202025)
# v.viewUp = (0.3130819684718471, 0.2445421036153976, 0.9177030241734793)
v.imageZoom = 1.0
SetView3D(v)

light = LightAttributes()
light.type = 1 # object
light.direction = (0, -0.75, -1)
light.brightness = 0.3
SetLight(1, light)

pyv.genPolarCoords2(dbs[2], 2, 10, 45, contours=True)

speciesStr = "Species: " + species
pyv.genTit( titS=speciesStr, Pos=(0.7,0.86), height=0.02 )
pyv.genTit( titS="Energies: All", Pos=(0.7,0.89), height=0.02 )
tit = pyv.genTit( titS=title, Pos=(0.25,0.955) )
pyv.cleanLegends(plXs,plYs,plTits, plHt=0.015)
pyv.setAtts(pWidth=1000, VidDir=tmpvid)

DrawPlots()

md = GetMetaData(dbs[2])
dt = md.times[1] - md.times[0]
pyv.doTimeLoop(Ninit=0, Nfin=None, T0=T0, dt=dt, Save=True, tLabPos=(0.35,0.05) )

outVid = "vid_r_phi_mag_" + varNames[vi] + "_all.mp4"
pyv.makeVid(outVid=outVid, vidDir=tmpvid, overwrite=True)