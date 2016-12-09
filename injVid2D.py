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
	xInj = "sInj"
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
else:
	#Multiple injection
	xInj = "mInj"
	h5pFile = ["pK70.h5part"]
	titS = ["H+ 70 keV"]
	Stubs = ["p70_mInj"]
	kevBds = [25,300]

Base = os.path.expanduser('~') + "/Work/Injection/"
Base = Base + "Data/"

EqDir = Base + "eqSlc_" + xInj #eqSlc database
pDir = Base + xInj #Directory of h5part

nFigs = range(len(titS))
Quiet = True


#dBz 
abBz = 25; 
dBzBds = [-abBz,abBz]

#Particles

pCMap = "Cool" #ColorTableNames()

if (Quiet):
	LaunchNowin()
else:
	Launch()

#Legends
plXs = [0.03]
plYs = [0.9,0.4]
plTits = ["Residual Bz [nT]","Particle Energy [keV]"]


#Do some defaults
pyv.lfmExprs()

for n in nFigs:
	#Construct filenames/directory structure
	Src0 = EqDir + "/eqSlc.*.vti database"
	Src1 = pDir + "/" + h5pFile[n]
	
	dbs = [Src0,Src1]
	
	md0 = GetMetaData(dbs[0])
	dt = md0.times[1] - md0.times[0]
	T0 = md0.times[0] - md0.times[0] #Reset to zero

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
	tit = pyv.genTit( titS=titS[n] )
	pyv.cleanLegends(plXs,plYs,plTits)
	pyv.setAtts()
	
	#Let's see what we got
	DrawPlots()
	
	#Do time loop
	pyv.doTimeLoop(T0=T0,dt=dt,Save=True,tLabPos=(0.3,0.05),Trim=True)
	
	outVid = Stubs[n] + ".mp4"
	pyv.makeVid(Clean=True,outVid=outVid,tScl=1)

	DeleteAllPlots()
	CloseDatabase(dbs[0])
	CloseDatabase(dbs[1])
	pyv.killAnnotations()
	os.system("mkdir tmpVid")

