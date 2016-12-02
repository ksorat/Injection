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

def getAf(h5pFile):
	pIds,Af = lfmpp.getH5pFin(h5pFile,"alpha")
	return Af

def getA0(h5pFile):
	pIds,A0 = lfmpp.getH5pInit(h5pFile,"alpha")
	return A0

def getdMu(h5pFile):
	TINY = 1.0
	pIds,Muf = lfmpp.getH5pFin(h5pFile ,"Mu")
	pIds,Mu0 = lfmpp.getH5pInit(h5pFile,"Mu")
	Ind = (Muf > TINY) & (Mu0 > TINY)
	Muf = Muf[Ind]
	Mu0 = Mu0[Ind]

	dMu = np.abs(Muf-Mu0)/Mu0
	#dMu = (Muf-Mu0)/Mu0

	print("\nCutting %d particles for undefined Mu"%(len(Ind)-Ind.sum()))
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


doKy = True #Do energization as y axis, or final pitch
doMux = True #Do delMu as x axis, or initial pitch


dMub = np.linspace(0,2)
dKb = np.linspace(0,6,60)
Ab = np.linspace(0,180,60)

cAxAf=[1.0e-4,5.0e-2]
cAxdK=[1.0e-2,1.0]

#Locations
RootDir = os.path.expanduser('~') + "/Work/Injection/Data"
vtiDir = RootDir + "/" + "eqSlc_" + Stub
h5pDir = RootDir + "/" + Stub

Ns = len(SpcsStubs)
Nk = len(KStubs)
lfmv.initLatex()

for s in range(Ns):
	for k in range(Nk):

		#Do 3 figures: dMu x dK, dMu x Af, A0 x dK
		h5p = SpcsStubs[s] + "_" + Stub + ".K" + str(KStubs[k]) + "." + h5Mid + ".h5part"
		h5pFile = h5pDir + "/" + h5p
		
		#Get changes
		print("Reading %s"%(h5p))
		dMu,Ind = getdMu(h5pFile)
		dK = getdK(h5pFile)
		Af = getAf(h5pFile)
		A0 = getA0(h5pFile)

		figStub = SpcsStubs[s] + "%02d"%KStubs[k]

		#Fig 1
		plt.hist2d(dMu,dK[Ind],[dMub,dKb],normed=True,norm=LogNorm(vmin=1.0e-2,vmax=1.0))
		plt.title('%s %02d (keV)'%(SpcsLab[s],KStubs[k]))
		plt.colorbar()
		plt.xlabel('Variation of 1st Invariant, $|\mu_{F}-\mu_{0}|/\mu_{0}$')
		plt.ylabel("Energization Fraction, $K_{F}/K_{0}$")
		plt.savefig(figStub + ".dMu_dK.png")
		plt.close('all')

		#Fig 2
		plt.hist2d(dMu,Af[Ind],[dMub,Ab],normed=True,norm=LogNorm(vmin=1.0e-4,vmax=5.0e-2))
		plt.title('%s %02d (keV)'%(SpcsLab[s],KStubs[k]))
		plt.colorbar()
		plt.xlabel('Variation of 1st Invariant, $|\mu_{F}-\mu_{0}|/\mu_{0}$')
		plt.ylabel("Final Pitch Angle")
		plt.savefig(figStub + ".dMu_Af.png")
		plt.close('all')

		#Fig 3
		plt.hist2d(A0,dK,[Ab,dKb],normed=True,norm=LogNorm(vmin=1.0e-4,vmax=1.0e-2))
		plt.title('%s %02d (keV)'%(SpcsLab[s],KStubs[k]))
		plt.colorbar()
		plt.xlabel("Initial Pitch Angle")
		plt.ylabel("Energization Fraction, $K_{F}/K_{0}$")
		plt.savefig(figStub + ".A0_dK.png")
		plt.close('all')

		#Fig 4
		plt.hist2d(A0,Af,[Ab,Ab],normed=True,norm=LogNorm(vmin=1.0e-6,vmax=1.0e-3))
		plt.title('%s %02d (keV)'%(SpcsLab[s],KStubs[k]))
		plt.colorbar()
		plt.xlabel("Initial Pitch Angle")
		plt.ylabel("Final Pitch Angle")
		plt.savefig(figStub + ".A0_Af.png")
		plt.close('all')
	
	
