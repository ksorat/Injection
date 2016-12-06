#Generate figures related to PDFs for multiple injection run

import numpy as np
import lfmPSD as lpsd
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

#First/Last steps
T0 = 0
Tf = 275
#Files
Root = os.path.expanduser('~') + "/Work/Injection/Data"
h5p = Root + "/mInj/p_mInj.All.h5part"

#Parameters for phase space
Lmin = 4
Lmax = 16
Nl = 30 #Number of L bins
Np = 20 #Number of phi bins
Na = 20 #Number of alpha bins
Kmin = 1
Kmax = 500 
Nk = 30 #Number of energy bins

#Create phase space
pSpc = lpsd.PhaseSpace(Lmin,Lmax,Nl,Np,Na,Kmin,Kmax,Nk)

#Load particle initial values and weight
p0 = lpsd.pState(h5p,T0)
lpsd.CalcWeights(p0,pSpc)

#Get final particle states, use p0 weights
pF = lpsd.pState(h5p,Tf)
pF.W = p0.W

#Calculate distribution functions
lpsd.calcPDF(pF,pSpc)
# #Look at initial state distribution at outer shell
# #W0,P0,A0,K0 = lpsd.shellCount(p0,9.9,0.2)

# #Look at final state at moderate shell
# #Wf,Pf,Af,Kf = lpsd.shellCount(pF,8,1)

# Ls = np.arange(5,12)
# dL = 1.0

# Nb = 80
# #Kb = np.logspace(1,3,Nb)
# Kb = np.linspace(10,850,Nb)

# NumPs = []
# bCs = []

# # for n in range(len(Ls)):
# # 	Wf,Kf,Muf = lpsd.shellCount(pF,Ls[n],dL)
# # 	NumP,bI = np.histogram(Kf,Kb,normed=True,weights=Wf)
# # 	NumPs.append(NumP)
# # 	bC = 0.5*(bI[0:-1]+bI[1:])
# # 	bCs.append(bC)
# # 	LabS = "%2.1f <= L <= %2.1f"%(Ls[n],Ls[n]+dL)
# # 	plt.loglog(bC,NumP,label=LabS)
# # plt.legend()
# # plt.show()

# #plt.hist(Kf,Kb,normed=True,weights=Wf,log=True)
# #plt.gca().set_xscale("log")
