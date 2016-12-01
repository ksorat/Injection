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

#Choose particles with energy above pCth percentile
def choosePs(h5pDir,h5pStub,pC=80,Np=12,doMask=False):
	#Find Np particles above energy Kc at end of simulation
	h5pFile = h5pDir + "/" + h5pStub

	if (doMask):
		isIn = lfmpp.getIn(h5pFile)
		pIds,Ks = lfmpp.getH5pFin(h5pFile,"kev",Mask=isIn)
	else:
		pIds,Ks = lfmpp.getH5pFin(h5pFile,"kev")
	Kc = np.percentile(Ks,pC)
	Ind = (Ks > Kc)
	pIds = pIds[Ind]
	Ks = Ks[Ind]
	
	Ntot = len(pIds)
	print("Found %d particles w/ final energy above %3.2f keV"%(Ntot,Kc))
	print("File = %s"%h5pFile)
	print("Maximum energy = %f"%Ks.max())
	print("Mean (K > Kc) energy = %f"%Ks.mean())
	print("\n\n")

	if (Ntot>=Np):
		
		IndR = np.random.choice(Ntot,Np,replace=False)
		pIds = pIds[IndR]
	else:
		print("Error, not enough matching particles found")
	return Kc,pIds

def getP(h5pDir,h5pStub,pId,vId="kev",tCut=1.0e+8):
	h5pFile = h5pDir + "/" + h5pStub
	
	t,x  = lfmpp.getH5pid(h5pFile,"x",pId)
	t,y  = lfmpp.getH5pid(h5pFile,"y",pId)
	t,V  = lfmpp.getH5pid(h5pFile,vId,pId)
	t,al = lfmpp.getH5pid(h5pFile,"alpha",pId)
	A0 = al[0]
	t0 = t[0]
	Ind = (t<=t0+tCut)

	return x[Ind],y[Ind],V[Ind],A0

#Particle data
Stub = "sInj"
h5Mid = "0001"

SpcsStubs = ["p","He","O"]
SpcsLab = ["H+","He++","O+"]

KStubs = [10,50,100]
pC = 95

doFast = False

np.random.seed(seed=31337)

#Traj data
#Nx = 6; Ny = 5
Nx = 4; Ny = 3
Tf = 500.0
DomX = [-15,2]
DomY = [-2,8]

#Field data
tSlc = 0

#Figure defaults
figSize = (10,10)
figQ = 300 #DPI

#Plot bounds fields/particles (nT/keV), plot details
fldBds = [-35,35]
Nc = 5
fldCMap = "RdGy_r"
fldOpac = 0.5
pCMap = "cool"
pSize = 4; pMark = 'o'; pLW = 0.1; pCLW = 0.2
pLab = "Energy [keV]"

#Gridspec defaults
hRat = list(4*np.ones(Nx+2))
hRat[0] = 0.25
hRat[-1] = 1

#Locations
RootDir = os.path.expanduser('~') + "/Work/Injection/Data"
vtiDir = RootDir + "/" + "eqSlc_" + Stub
h5pDir = RootDir + "/" + Stub


Ns = len(SpcsStubs)
Nk = len(KStubs)
lfmv.initLatex()
xi,yi,dBz = getFld(vtiDir,tSlc)
Bv = np.linspace(fldBds[0],fldBds[1],Nc)

for s in range(Ns):
	for k in range(Nk):
		h5p = SpcsStubs[s] + "_" + Stub + ".K" + str(KStubs[k]) + "." + h5Mid + ".h5part"

		figName = SpcsStubs[s] + str(KStubs[k]) + ".%02dTrjs.png"%(Nx*Ny)
		titS = "Sampled High-Energy Trajectories for %s %02d keV"%(SpcsLab[s],KStubs[k])
		
		
		#Pick particles
		Kc,pIds = choosePs(h5pDir,h5p,pC=pC,Np=Nx*Ny)
		KcB = np.ceil(Kc/5)*5 #Round to nearest 5th
		pBds = [0,KcB]
		print(pIds)

		#Do figures
		fig = plt.figure(figsize=figSize,tight_layout=True)
		gs = gridspec.GridSpec(Nx+2,Ny,height_ratios=hRat)

		n = 0
		
		for i in range(1,Nx+1):
			for j in range(Ny):
				
				Ax = fig.add_subplot(gs[i,j])
		
				if (i == Nx):
					plt.xlabel("GSM-X [Re]",fontsize="small")
				else:
					plt.setp(Ax.get_xticklabels(),visible=False)
				if (j == 0):
					plt.ylabel("GSM-Y [Re]",fontsize="small")
				else:
					plt.setp(Ax.get_yticklabels(),visible=False)
					
				fldPlt = Ax.pcolormesh(xi,yi,dBz,vmin=fldBds[0],vmax=fldBds[1],cmap=fldCMap,shading='gouraud',alpha=fldOpac)
				#fldPlt = Ax.pcolormesh(xi,yi,dBz,vmin=fldBds[0],vmax=fldBds[1],cmap=fldCMap)
				#plt.contour(xi,yi,dBz,Bv,cmap=fldCMap)
				lfmv.addEarth2D()
		
				#Now do particles
				if (n == 0 or not doFast):
					
					xs,ys,zs,A0 = getP(h5pDir,h5p,pIds[n],tCut=Tf)
		
				pPlt = Ax.scatter(xs,ys,s=pSize,marker=pMark,c=zs,vmin=pBds[0],vmax=pBds[1],cmap=pCMap,linewidth=pLW)
				Leg = ["ID %d\nK = %3.2f (keV)\n$\alpha_{0}$ = %2.2f$^{\circ}$"%(pIds[n],zs.max(),A0)]
				plt.legend(Leg,loc="lower left",fontsize="xx-small",scatterpoints=1,markerscale=0,frameon=False)
		
				plt.plot(xs,ys,'w-',linewidth=pCLW)
				plt.axis('scaled')
				plt.xlim(DomX); plt.ylim(DomY)
				plt.tick_params(axis='both', which='major', labelsize=6)
				plt.tick_params(axis='both', which='minor', labelsize=4)
				
				n=n+1
		
		AxCbar = plt.subplot(gs[-1,:])
		plt.colorbar(pPlt, cax=AxCbar,orientation='horizontal',label=pLab)
		plt.suptitle(titS,fontsize="large")
		gs.tight_layout(fig)
		plt.savefig(figName,dpi=figQ)
		plt.close('all')

