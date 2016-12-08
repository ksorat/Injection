
#Generate energy histograms
import os
import numpy as np
import lfmViz as lfmv
import lfmPostproc as lfmpp
import matplotlib as mpl
import matplotlib.pyplot as plt

#Particle data
Stub = "sInj"
SpcsStubs = ["p","Hepp","O"]
SpcsLab = ["H+","He++","O+"]
KStubs = [10,50,100]

Nb = 25
Kmax = [250,500,750]

#Locations
RootDir = os.path.expanduser('~') + "/Work/Injection/Data"
vtiDir = RootDir + "/" + "eqSlc"
h5pDir = RootDir + "/" "sInj"

Ns = len(SpcsStubs)
Nk = len(KStubs)

lfmv.initLatex()

for k in range(Nk):
	Ks = []
	Leg = []
	for s in range(Ns):
		h5p = SpcsStubs[s] + "_" + Stub + ".K%02d"%KStubs[k] + ".0001.h5part"
		figName = "K%02d"%KStubs[k] + ".kHist.png"
		h5pFile = h5pDir + "/" + h5p
		print("Reading %s"%h5pFile)

		Leg.append("%s %02d keV"%(SpcsLab[s],KStubs[k]))
		#Get final particle energies
		pIds,K = lfmpp.getH5pFin(h5pFile,"kev")
		print("%s / K0 = %02d"%(SpcsLab[s],KStubs[k]))
		print("\tMean K = %f"%K.mean())
		print(" \tMax K = %f"%K.max())
		print(" \tMin K = %f"%(K.min()))
		Ks.append(K)

	bins = np.linspace(0,Kmax[k],Nb)
	plt.hist(Ks,bins,normed=True,log=True)
	plt.legend(Leg)
	plt.xlabel("Final Energy [keV]")
	plt.ylabel("Population Density")
	plt.savefig(figName)
	plt.close('all')


