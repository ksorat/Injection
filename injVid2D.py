import sys
import os
import numpy as np
import datetime
from visit import *
from visit_utils import *
from visit_utils.common import lsearch #lsearch(dir(),"blah")
import pyVisit as pyv


Spc = "H+"
h5pStub = "pInj"

Base = os.path.expanduser('~') + "/Work/Injection/"
Base = Base + "Data/Long/"

EqDir = Base + "eqSlc/" #eqSlc database
pDir = Base + "H5p" #Directory of h5part

Quiet = True

titS = "%s Injection"%(Spc)

#dBz 
abBz = 25; 
dBzBds = [-abBz,abBz]

#Particles
kevBds = [10,200]
pCMap = "Cool" #ColorTableNames()

if (Quiet):
	LaunchNowin()
else:
	Launch()

#Legends
plXs = [0.03]
plYs = [0.9,0.4]
plTits = ["Residual Bz [nT]","Particle Energy [keV]"]

#Construct filenames/directory structure
Src0 = EqDir + "/eqSlc.*.vti database"
Src1 = pDir + "/" + h5pStub + ".All.h5part"
dbs = [Src0,Src1]

md0 = GetMetaData(dbs[0])
dt = md0.times[1] - md0.times[0]
T0 = md0.times[0] - md0.times[0] #Reset to zero

print(Src1,T0,dt)
#Do some defaults
pyv.lfmExprs()

#Open databases
OpenDatabase(dbs[0])
OpenDatabase(dbs[1])


#Create database correlation
CreateDatabaseCorrelation("P2Fld",dbs,0)

DefineScalarExpression("isIn","in")

#Create fields/particle plots
pyv.lfmPCol(dbs[0],"dBz",vBds=dBzBds,pcOpac=0.7,Inv=True)
pyv.lfmPScat(dbs[1],v4="kev",vBds=kevBds,cMap=pCMap,Inv=False)

#Cutout
ActivateDatabase(dbs[1])
SetActivePlots( (1) )
pyv.onlyIn()

#Gussy things up
tit = pyv.genTit( titS=titS )
pyv.cleanLegends(plXs,plYs,plTits)
pyv.setAtts()

#Let's see what we got
DrawPlots()

#Do time loop
pyv.doTimeLoop(T0=T0,dt=dt,Save=True,tLabPos=(0.3,0.05),Trim=True)
outVid = h5pStub + ".mp4"
pyv.makeVid(Clean=True,outVid=outVid,tSlc=3)
