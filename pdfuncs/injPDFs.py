#Generate figures related to PDFs for multiple injection run

import numpy as np
import lfmPSD as lpsd
import lfmViz as lfmv
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os
import cPickle as pickle

#Load or calculate
#doCalc = False
doCalc = True
sStub = "O"
#fPkl = "pdfunc.pkl"
fPkl = "pdfunc.%s.pkl"%(sStub)

#First/Last steps
T0 = 0
Tf = 275
#Files
Root = os.path.expanduser('~') + "/Work/Injection/Data"

h5p = Root + "/mInj/" + sStub + "_mInj.eqAll.h5part"

print("Reading %s"%(h5p))
#Parameters for phase space
Lmin = 4
Lmax = 16
Nl = 48 #Number of L bins
Np = 40 #Number of phi bins
Na = 20 #Number of alpha bins
Kmin = 1
Kmax = 750 
Nk = 50 #Number of energy bins
Nmu = 50

if (doCalc):
	#Create phase space
	pSpc = lpsd.PhaseSpace(Lmin,Lmax,Nl,Np,Na,Kmin,Kmax,Nk)
	
	#Load particle initial values and weight
	p0 = lpsd.pState(h5p,T0)
	lpsd.CalcWeights(p0,pSpc)
	
	#Get final particle states, use p0 weights
	pF = lpsd.pState(h5p,Tf)
	pF.W = p0.W
	
	#Calculate distribution functions
	lpsd.calcPDF(pF,pSpc,muMin=30.0,muMax=1.0e+5,Nmu=Nmu)

	#Save to pickle
	print("Writing pickle")
	with open(fPkl,"wb") as f:
		pickle.dump(pSpc,f)
		pickle.dump(p0,f)
		pickle.dump(pF,f)
else:
	#Read from pickle
	print("Loading data")
	with open(fPkl, "rb") as f:
		pSpc = pickle.load(f)
		p0   = pickle.load(f)
		pF   = pickle.load(f)

lfmv.initLatex()

lpsd.genDistPic(pF,doMu=True,oStub=sStub)
lpsd.genDistPic(pF,doMu=False,oStub=sStub)

