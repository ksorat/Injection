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

for n in range(Nf):
	fIn = Files[n]
	fOut = fOuts[n]
	
	t,K = getH5p(fIn,"kev")
	t,Mu = getH5p(fIn,"Mu")

	dK = K[2:-2,:] - K[0:-4,:]
	dlK = dK/(dt*K[1:-3,:])

	dMu = Mu[2:-2,:] - Mu[0:-4,:]
	dlMu = dMu/(dt*Mu[1:-3,:])

	#Restrict to good values
	Ind = (Mu[1:-3] < 1.0e-8) & (np.isnan(Mu[1:-3]))
	dlMu[Ind] = 0.0
	dlK[Ind] 0.0

	plt.hist2d(dlMu,dlK,normed=True)

	plt.savefig(fOut,dpi=figQ)
	plt.close('all')