import sys
import os
import numpy as np
import datetime
from visit import *
from visit_utils import *
from visit_utils.common import lsearch #lsearch(dir(),"blah")
import pyVisit as pyv


doSinj = False

if (doSinj):
	
	h5pFile = ["p_sInj.K50.0001.h5part","p_xlInJ.K50.0001.h5part",
		"Hepp_sInj.K50.0001.h5part","Hepp_xlInj.K50.0001.h5part",
		"O_sInj.K50.0001.h5part","O_xlInJ.K50.0001.h5part"]
	
	titS = ["H+ 50 keV Injection","H+ 50 keV (XL) Injection",
		"He++ 50 keV Injection","He++ 50 keV (XL) Injection",
		"O+ 50 keV Injection","O+ 50 keV (XL) Injection"]
	
	Stubs =["p50_sInj","p50xl_sInj",
		"He50_sInj","He50xl_sInj",
		"O50_sInj","O50xl_sInj"]
	kevBds = [10,200]
	vID = "kev"
else:
	#Multiple injection
	xInj = "mInj"
	#h5pFile = ["p_mInj.eqAll.h5part"]
	#titS = ["H+ 70 keV"]
	#Stubs = ["p70_mInj"]
	# h5pFile = ["O_mInj.eqAll.h5part"]
	# titS = ["O+ 70 keV"]
	# Stubs = ["O70_mInj"]
	h5pFile = ["Hepp_mInj.eqAll.h5part"]
	titS = ["He++ 70 keV"]
	Stubs = ["He70_mInj"]

	kevBds = [25,300]
	vID = "keveq"
	K0 = 70

xInj = "csInj"
DefineScalarExpression("ev","kev*1.0e-3")
DefineScalarExpression("isIn","in")

vId = "ev"
vBds = [0,10]

h5Ps = ["Hep_csInj.K0.0001.h5part",  "Hepp_csInj.K0.0001.h5part",
        "O_csInj.K0.0001.h5part", "p_csInj.K0.0001.h5part"]
sLabs = ["He+","He++","O+","H+"]

doSpc = [3,0,1]
cMaps = ["Blues","Purples","Greens","Oranges"]

Base = os.path.expanduser('~') + "/Work/Injection/"
Base = Base + "Data/"

EqDir = Base + "eqSlc_" + xInj #eqSlc database
pDir = Base + xInj #Directory of h5part

Quiet = True


#dBz 
abBz = 25; 
dBzBds = [-abBz,abBz]

#Particles
vID = "kev"
titS = ["Cold Particle Injection"]

if (Quiet):
	LaunchNowin()
else:
	Launch()

Ns = len(doSpc)

#Legends/DBs
Src0 = EqDir + "/eqSlc.*.vti database"
plTits = ["Residual Bz [nT]"]
dbs = [Src0]
for s in doSpc:
	lS = "%s Energy [eV]"%(sLabs[s])
	plTits.append(lS)
	SrcS = pDir + "/" + h5Ps[s]
	dbs.append(SrcS)
print(plTits,SrcS)

plXs = [0.03]
plYs = [0.9,0.4,0.2,0.7]

#Do some defaults
pyv.lfmExprs()

	
md0 = GetMetaData(dbs[0])
dt = md0.times[1] - md0.times[0]
T0 = md0.times[0] - md0.times[0] #Reset to zero

#Open databases
for db in dbs:
	OpenDatabase(db)	
	
#Create database correlation
CreateDatabaseCorrelation("P2Fld",dbs,0)

	
#Create fields/particle plots
pyv.lfmPCol(dbs[0],"dBz",vBds=dBzBds,pcOpac=0.7,Inv=True)
for n in range(Ns):
	db = dbs[n+1]
	pCMap = cMaps[n]
	pyv.lfmPScat(db,v4=vID,vBds=vBds,cMap=pCMap,Inv=False)
	
#Cutout
ActivateDatabase(dbs[1])
SetActivePlots( (1) )
pyv.onlyIn()
		
#Gussy things up
tit = pyv.genTit( titS=titS[n] )
pyv.cleanLegends(plXs,plYs,plTits)
pyv.setAtts()

#Let's see what we got
DrawPlots()
SaveWindow()

# #Do time loop
# pyv.doTimeLoop(T0=T0,dt=dt,Save=True,tLabPos=(0.3,0.05),Trim=True)

# outVid = Stubs[n] + ".mp4"
# pyv.makeVid(Clean=True,outVid=outVid,tScl=1)
# DeleteAllPlots()
# CloseDatabase(dbs[0])
# CloseDatabase(dbs[1])
# pyv.killAnnotations()
# os.system("mkdir tmpVid")

