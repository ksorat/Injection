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
Lmax = 15
Nl = 30 #Number of L bins
Np = 20 #Number of phi bins
Na = 20 #Number of alpha bins
Kmin = 10
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

