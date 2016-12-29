import os
import numpy as np
import lfmViz as lfmv
import lfmPostproc as lfmpp
import matplotlib as mpl
import matplotlib.pyplot as plt


Root = os.path.expanduser('~') + "/Work/Injection/Data/csInj/"
Tail = "_csInj.K0.0001.h5part"
Stubs = ["p","Hep","Hepp","O"]
Labs = ["H+","He+","He++","O+"]
Plts = ["b","g","r","c"]
titS = "Single Injection (1 eV)"

figName = "cs_Kt.png"
figQ = 300
pC = [50,95,99]

Ns = len(Stubs)
Np = len(pC)
for n in range(Ns):
	fIn = Root + Stubs[n] + Tail

	t,Kev = lfmpp.getH5p(fIn,"kev")
	K = Kev
	Kb = K.mean(axis=1) #Average(t)
	dK = K.std(axis=1) #Std
	for i in range(Np):
		pLab = "_"
		if (i == 0):
			pLab = "%s, %s Percentiles"%(Labs[n],str(pC))
		Kc = np.percentile(K,pC[i],axis=1)
		plt.plot(t,Kc,Plts[n],label=pLab)
	
	
	#plt.errorbar(t,Kb,dK,label=Labs[n],errorevery=10)
	#plt.plot(t,Kc,label=Labs[n])
	print("Spc = %s"%(Labs[n]))
	print("\tMax = %f"%(K.max()))
	print("\tMin = %f"%(K.min()))
	print("\tNANs = %d"%(np.isnan(K).sum()))
plt.xlabel("Time [s]")
plt.ylabel("Energy [keV]")
plt.legend(fontsize="xx-small")
plt.xlim(1750,2250)
plt.savefig(figName,dpi=figQ)