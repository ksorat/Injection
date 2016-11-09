#Generates trajectory panel figure

import numpy as np
import os
import lfmViz as lfmv
import lfmPostproc as lfmpp
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Wedge

def getFld(vtiDir,t,dt=10.0,eqStub="eqSlc"):
	tSlc = np.int(t/dt)
	vtiFile = vtiDir + "/" + eqStub + ".%04d.vti"%(tSlc)

	dBz = lfmv.getVTI_SlcSclr(vtiFile).T
	ori,dx,ex = lfmv.getVTI_Eq(vtiFile)
	xi = ori[0] + np.arange(ex[0],ex[1]+1)*dx[0]
	yi = ori[1] + np.arange(ex[2],ex[3]+1)*dx[1]

	return xi,yi,dBz

def choosePs(h5pDir,h5pStub,Kc=100,Np=12,doMask=False):
	#Find Np particles above energy Kc at end of simulation
	h5pFile = h5pDir + "/" + h5pStub

	if (doMask):
		isIn = lfmpp.getIn(h5pFile)
		pIds,Ks = lfmpp.getH5pFin(h5pFile,"kev",Mask=isIn)
	else:
		pIds,Ks = lfmpp.getH5pFin(h5pFile,"kev")
	Ind = Ks>Kc

	pIds = pIds[Ind]
	Ks = Ks[Ind]
	Ntot = len(pIds)
	print("Found %d particles w/ final energy above %3.2f keV"%(Ntot,Kc))
	print("Maximum energy = %f"%Ks.max())
	print("Mean (K > Kc) energy = %f"%Ks.mean())
	if (Ntot>=Np):
		
		IndR = np.random.choice(Ntot,Np,replace=False)
		pIds = pIds[IndR]
	else:
		print("Error, not enough matching particles found")
	return pIds
def getP(h5pDir,h5pStub,pId,vId="kev",tCut=1.0e+8):
	h5pFile = h5pDir + "/" + h5pStub
	
	t,x = lfmpp.getH5pid(h5pFile,"x",pId)
	t,y = lfmpp.getH5pid(h5pFile,"y",pId)
	t,V = lfmpp.getH5pid(h5pFile,vId,pId)

	t0 = t[0]
	Ind = (t<=t0+tCut)

	return x[Ind],y[Ind],V[Ind]

#Particle data
s0 = 0
Spcs = ["H+ 50 keV"]
h5ps = ["Inj50.All.h5part"]

Nx = 5
Ny = 4
Kc = 200
Tf = 500.0

#Field data
tSlc = 0

figSize = (10,10)
figQ = 300 #DPI
figName = "trjPanel.png"

DomX = [-15,2]
DomY = [-2,8]

#Plot bounds fields/particles (nT/keV), plot details
fldBds = [-35,35]
Nc = 5
fldCMap = "RdGy_r"
fldOpac = 0.5

pBds = [0,Kc]
pCMap = "cool"
pSize = 10; pMark = 'o'; pLW = 1
pLab = "Energy [keV]"
#Locations
RootDir = "/Users/Kareem/Work/Injection/Data"
vtiDir = RootDir + "/" + "eqSlc"
h5pDir = RootDir + "/" "H5p"

#Pick particles
pIds = choosePs(h5pDir,h5ps[s0],Kc=Kc,Np=Nx*Ny)
print(pIds)

#Do figures
hRat = list(4*np.ones(Nx+2))
hRat[0] = 0.25
hRat[-1] = 1
#lfmv.initLatex()
fig = plt.figure(figsize=figSize,tight_layout=True)

gs = gridspec.GridSpec(Nx+2,Ny,height_ratios=hRat)

xi,yi,dBz = getFld(vtiDir,tSlc)

plot.tick_params(axis='both', which='major', labelsize=10)
plot.tick_params(axis='both', which='minor', labelsize=8)
n = 0
Bv = np.linspace(fldBds[0],fldBds[1],Nc)
for i in range(1,Nx+1):
	for j in range(Ny):
		
		Ax = fig.add_subplot(gs[i,j])

		if (i == Nx):
			plt.xlabel("GSM-X [Re]",fontsize=small)
		else:
			plt.setp(Ax.get_xticklabels(),visible=False)
		if (j == 0):
			plt.ylabel("GSM-Y [Re]",fontsize=small)
		else:
			plt.setp(Ax.get_yticklabels(),visible=False)


		fldPlt = Ax.pcolormesh(xi,yi,dBz,vmin=fldBds[0],vmax=fldBds[1],cmap=fldCMap,shading='gouraud',alpha=fldOpac)
		#fldPlt = Ax.pcolormesh(xi,yi,dBz,vmin=fldBds[0],vmax=fldBds[1],cmap=fldCMap)
		#plt.contour(xi,yi,dBz,Bv,cmap=fldCMap)
		lfmv.addEarth2D()

		#Now do particles
		xs,ys,zs = getP(h5pDir,h5ps[s0],pIds[n],tCut=Tf)

		pPlt = Ax.scatter(xs,ys,s=pSize,marker=pMark,c=zs,vmin=pBds[0],vmax=pBds[1],cmap=pCMap,linewidth=pLW)
		Leg = ["ID %d\nK = %3.2f (keV)"%(pIds[n],zs.max())]
		plt.legend(Leg,loc="lower left",fontsize="xx-small",scatterpoints=1,markerscale=0,markerfirst=False,frameon=False)

		plt.plot(xs,ys,'w-',linewidth=0.2)
		plt.axis('scaled')
		plt.xlim(DomX); plt.ylim(DomY)
		
		n=n+1

AxCbar = plt.subplot(gs[-1,:])
plt.colorbar(pPlt, cax=AxCbar,orientation='horizontal',label=pLab)
plt.suptitle("Sampled High-Energy Trajectories for %s"%Spcs[s0],fontsize="large")
gs.tight_layout(fig)
plt.savefig(figName,dpi=figQ)

