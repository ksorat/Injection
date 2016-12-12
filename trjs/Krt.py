#Plot energy/L shell as a function of time for specific high energization particles
import numpy as np
import os
import lfmViz as lfmv
import lfmPostproc as lfmpp
import matplotlib as mpl
import matplotlib.pyplot as plt



Base = os.path.expanduser('~') + "/Work/Injection/Data/" + "sInj/"
h5Ps = ["p_sInj.K10.0001.h5part","Hepp_sInj.K10.0001.h5part"]
pIDs = [[1710,3659,33053,33051],[256,25779,15417,7472]]
sLab = ["H+","He++"]
pC = ["b","g","r","c","m","darkorange","lightslategray","purple"]
pC = ["blue","slateblue","cyan","lightsteelblue",
	"lime","darkgreen","lightgreen","greenyellow"]


LW = 0.5


figSize = (10,10)
figQ = 300 #DPI
figName = "Klt.png"

Ns = len(h5Ps)
Np = len(pIDs[0])

fig,Ax = plt.subplots(figsize=figSize,nrows=2,sharex=False)
#Ax2 = Ax1.twinx()

Ax1 = Ax[0]
Ax2 = Ax[1]

ns = 0
for s in range(Ns):
	h5P = Base + h5Ps[s]
	ids = pIDs[s]
	for n in range(Np):
		idn = ids[n]
		t,K = lfmpp.getH5pid(h5P,"kev",idn)
		t,xeq = lfmpp.getH5pid(h5P,"xeq",idn)
		t,yeq = lfmpp.getH5pid(h5P,"yeq",idn)
		L = np.sqrt(xeq**2.0 + yeq**2.0)
		pT = pC[ns]

		Lab = "%s (%d)"%(sLab[s],idn)
		Ax1.plot(t,K,pT,label=Lab,linewidth=LW)
		Ax2.plot(t,L,pT,linewidth=LW)
		ns = ns+1
Ax1.legend(loc="lower right",fontsize="small",ncol=2)
Ax1.set_xlabel('Time [s]')
Ax2.set_xlabel('Time [s]')
Ax1.set_ylabel('Energy [keV]')
Ax2.set_ylabel('Radius of Eq. Crossing [Re]')

plt.savefig(figName,dpi=figQ)
