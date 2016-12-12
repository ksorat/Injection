#Plot energy/L shell as a function of time for specific high energization particles
import numpy as np
import os
import lfmViz as lfmv
import lfmPostproc as lfmpp
import matplotlib as mpl
import matplotlib.pyplot as plt



Base = os.path.expanduser('~') + "/Work/Injection/Data" + "sInj/"
h5Ps = ["p_sInj.K10.0001.h5part","Hepp_sInj.K10.0001.h5part"]
pIDs = [[1710,3659,33053,33051],[256,25779,15417,7472]]
sLab = ["H+","He++"]
pC = ["b","g"]
pMrk = ["o","x","s","*"]

figSize = (10,10)
figQ = 300 #DPI
figName = "Klt.png"

Ns = len(h5Ps)
Np = len(pIDs[0])

fig,Ax1 = plt.subplots(figsize=figSize)
Ax2 = Ax1.twinx()

for s in range(Ns):
	h5P = Base + h5Ps[s]
	ids = pIDs[s]
	for n in range(Np):
		idn = ids[n]
		t,K = lfmpp.getH5pid(h5P,"kev",idn)
		t,xeq = lfmpp.getH5pid(h5P,"xeq",idn)
		t,yeq = lfmpp.getH5pid(h5P,"yeq",idn)
		L = np.sqrt(xeq**2.0 + yeq**2.0)

		pT1 = pC[s] + pMrk[n] + "-"
		pT2 = pC[s] + pMrk[n] + "--"
		Lab = "%s (%d)"%(sLab[s],idn)
		Ax1.plot(t,K,pT1,label=Lab)
		Ax2.plot(t,L,pT2)


plt.savefig(figName,dpi=figQ)
