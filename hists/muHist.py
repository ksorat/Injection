#Generate mu histograms
import os
import numpy as np
import lfmViz as lfmv
import lfmPostproc as lfmpp
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def getdK(h5pFile):
	pIds,Kf = lfmpp.getH5pFin(h5pFile,"kev")
	pIds,K0 = lfmpp.getH5pInit(h5pFile,"kev")
	dK = Kf/K0
	return dK

def getdMu(h5pFile):
	TINY = 1.0
	pIds,Muf = lfmpp.getH5pFin(h5pFile ,"Mu")
	pIds,Mu0 = lfmpp.getH5pInit(h5pFile,"Mu")
	Ind = (Muf > TINY) & (Mu0 > TINY)
	Muf = Muf[Ind]
	Mu0 = Mu0[Ind]

	#dMu = np.abs(Muf-Mu0)/Mu0
	dMu = (Muf-Mu0)/Mu0
	print("Cutting %d particles for undefined Mu"%(len(Ind)-Ind.sum()))
	print("Min dMu = %f"%(dMu.min()))
	print("Min Muf = %f, Min Mu0 = %f"%(Muf.min(),Mu0.min()))
	print("\n\n")
	return dMu,Ind

#Particle data
Stub = "sInj"
h5Mid = "0001"

SpcsStubs = ["p","He","O"]
SpcsLab = ["H+","He++","O+"]
KStubs = [10,50,100]



dMub = np.linspace(-2,2)
dKb = np.linspace(0,6,60)
cAx=[1.0e-2,5]

#Locations
RootDir = os.path.expanduser('~') + "/Work/Injection/Data"
vtiDir = RootDir + "/" + "eqSlc_" + Stub
h5pDir = RootDir + "/" + Stub

Ns = len(SpcsStubs)
Nk = len(KStubs)
lfmv.initLatex()

for s in range(Ns):
	for k in range(Nk):
		h5p = SpcsStubs[s] + "_" + Stub + ".K" + str(KStubs[k]) + "." + h5Mid + ".h5part"
		figName = SpcsStubs[s] + "%02d"%KStubs[k] + ".muHist.png"
		h5pFile = h5pDir + "/" + h5p
		
		#Get changes
		print("Reading %s"%(h5p))
		dMu,Ind = getdMu(h5pFile)
		dK  = getdK (h5pFile)
		dK = dK[Ind]

		#plt.scatter(dMu,dK)
		plt.hist2d(dMu,dK,[dMub,dKb],normed=True,norm=LogNorm(vmin=cAx[0],vmax=cAx[1]))
		#Ax = plt.gca()
		#Ax.set_xscale('log')
		plt.colorbar()
		plt.title('%s %02d (keV)'%(SpcsLab[s],KStubs[k]))
		plt.xlabel('Variation of 1st Invariant, $|\mu_{F}-\mu_{0}|/\mu_{0}$')
		#plt.xlabel('Variation of 1st Invariant')
		plt.ylabel("Energization Fraction, $K_{F}/K_{0}$")
		plt.savefig(figName)
		plt.close('all')
	
	
