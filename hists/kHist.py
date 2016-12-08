
#Generate energy histograms
import os
import numpy as np
import lfmViz as lfmv
import lfmPostproc as lfmpp
import matplotlib as mpl
import matplotlib.pyplot as plt

#Particle data
Stub = "Inj"
SpcsStubs = ["p","Hepp","O"]
SpcsLab = ["H+","He++","O+"]
KStubs = [10,50,100]

Nb = 50
k0 = 0; k1 = 300

#Locations
RootDir = os.path.expanduser('~') + "/Work/Injection/Data"
vtiDir = RootDir + "/" + "eqSlc"
h5pDir = RootDir + "/" "H5p"

Ns = len(SpcsStubs)
Nk = len(KStubs)
bins = np.linspace(k0,k1,Nb)
lfmv.initLatex()

for k in range(Nk):
	Ks = []
	Leg = []
	for s in range(Ns):
		h5p = SpcsStubs[s] + Stub + "%02d"%KStubs[k] + ".0001.h5part"
		figName = SpcsStubs[s] + ".kHist.png"
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

	plt.hist(Ks,bins,normed=True)
	plt.legend(Leg)
	plt.xlabel("Final Energy [keV]")
	plt.ylabel("Population Density")
	plt.savefig(figName)
	plt.close('all')


