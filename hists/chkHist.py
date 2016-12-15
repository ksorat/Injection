#History of energies for charge differences

import os
import numpy as np
import lfmViz as lfmv
import lfmPostproc as lfmpp
import matplotlib as mpl
import matplotlib.pyplot as plt


Root = os.path.expanduser('~') + "/Work/Injection/Data/sInj/"
Tail = "_sInj.K10.0001.h5part"
Stubs = ["p","Hep","Hepp","O"]
Labs = ["H+","He+","He++","O+"]
titS = "Single Injection (10 keV)"

N = len(Stubs)

Ks = []
figName = "chK.png"
figQ = 300
K0 = 1; K1 = 250
Nb = 120

for n in range(N):
	h5p = Root + Stubs[n] + Tail
	pIds,K = lfmpp.getH5pFin(h5p,"kev")

	Ks.append(K)

bins = np.linspace(K0,K1,Nb)
plt.hist(Ks,bins,normed=False,log=True,stacked=True,histtype='step',fill=True)
plt.legend(Labs)
plt.xlabel("Final Energy [keV]")
plt.ylabel("Count")
plt.title(titS)
plt.savefig(figName,dpi=figQ)
plt.close('all')