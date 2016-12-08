#Generate histograms for dLM/dt and dlK/dt

import os
import numpy as np
import lfmViz as lfmv
import lfmPostproc as lfmpp
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm

#Locations
RootDir = os.path.expanduser('~') + "/Work/Injection/Data/sInj/"

Files = ["O_sInj.K50.0001.h5part"]
fOuts = ["O50.mk.png"]
#Figure details
figSize = (10,10)
figQ = 300 #DPI

lfmv.initLatex()

Nf = len(Files)
dt = 1.0

dkB = np.linspace(-1,1,100)
dmB = np.linspace(-1,1,100)
hNorm = LogNorm(vmin=1.0e-4,vmax=1.0e+2)


#Create Files/fOuts/TitS
Files = []
fOuts = []
TitS = []
K = [10,50,100]
Spc = ["p","Hepp","O"]
sLab = ["H+","He++","O+"]

for k in range(len(K)):
	for s in range(len(Spc)):
		Files.append("%s_sInj.K%02d.0001.h5part"%(Spc[s],K[k]))
		fOuts.append("%s%02d.mk.png"%(Spc[s],K[k]))
		TitS.append("%s %02d keV"(%sLab[s],K[k]))

for n in range(Nf):
	fIn = RootDir + Files[n]
	fOut = fOuts[n]

	t,K = lfmpp.getH5p(fIn,"kev")
	t,Mu = lfmpp.getH5p(fIn,"Mu")

	dK = K[2:-2,:] - K[0:-4,:]
	dlK = dK/(dt*K[1:-3,:])

	dMu = Mu[2:-2,:] - Mu[0:-4,:]
	dlMu = dMu/(dt*Mu[1:-3,:])

	muf = Mu[1:-3,:].flatten()
	dm = dlMu.flatten()
	dk = dlK.flatten()

	#Restrict to good values
	Ind = (muf > 1.0e-8) &  (~ np.isnan(muf))
	dm = dm[Ind]
	dk = dk[Ind]

	Ind = ( ~ np.isnan(dm) )
	dm = dm[Ind]
	dk = dk[Ind]

	# #Restrict to good values
	# Ind = (Mu[1:-3,:] < 1.0e-8) | (np.isnan(Mu[1:-3,:]))
	# dlMu[Ind] = 0.0
	# dlK[Ind] = 0.0

	# dm = dlMu.flatten()
	# dk = dlK.flatten()

	plt.hist2d(dm,dk,[dmB,dkB],normed=True,norm=hNorm)
	plt.colorbar()
	plt.xlabel('dlog($\mu$)/dt')
	plt.ylabel('dlog(K)/dt')
	plt.title(TitS[n])
	plt.savefig(fOut,dpi=figQ)
	plt.close('all')
