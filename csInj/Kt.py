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
titS = "Single Injection (1 eV)"

figName = "cs_Kt.png"
figQ = 300
pC = 95
Ns = len(Stubs)
for n in range(Ns):
	fIn = Root + Stubs[n] + Tail

	t,Kev = lfmpp.getH5p(fIn,"kev")
	K = 1.0e+3*Kev
	Kb = K.mean(axis=1) #Average(t)
	dK = K.std(axis=1) #Std
	Kc = np.percentile(K,pC,axis=1)
	plt.errorbar(t,Kb,dK,label=Labs[n],errorevery=10)
	#plt.plot(t,Kc,label=Labs[n])
	print("Spc = %s"%(Labs[n]))
	print("\tMax = %f"%(K.max()))
	print("\tMin = %f"%(K.min()))
plt.legend()
plt.savefig(figName,dpi=figQ)