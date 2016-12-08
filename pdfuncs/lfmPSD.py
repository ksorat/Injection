#Various routines to generate phase space densities from lfmtp runs

import numpy as np
import lfmPostproc as lfmpp
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec

#Generate phase space
#Take in Lmin/Lmax,Nl
#Take in Nphi
#Take in Nalpha
#Take in initial energy values
class PhaseSpace(object):
	def __init__(self,Lmin,Lmax,Nl,Np,Na,Kmin,Kmax,Nk):

		#Construct various dimensions
		self.Li = np.linspace(Lmin,Lmax,Nl+1)
		self.Lc = 0.5*(self.Li[0:-1] + self.Li[1:])
		self.Nl = Nl
		self.dl = 1.0*(Lmax-Lmin)/Nl

		self.Pi = np.linspace(0,360,Np+1)
		self.Pc = 0.5*(self.Pi[0:-1] + self.Pi[1:])
		self.Np = Np
		self.dp = 1.0*(360-0)/Np

		self.Ai = np.linspace(0,180,Na+1)
		self.Ac = 0.5*(self.Ai[0:-1] + self.Ai[1:])
		self.Na = Na
		self.da = 1.0*(180-0)/Na

		self.Ki = np.logspace(np.log10(Kmin),np.log10(Kmax),Nk+1)
		self.Kc = 0.5*(self.Ki[0:-1] + self.Ki[1:])
		self.Nk = Nk
		self.dk = self.Ki[1:]-self.Ki[0:-1]

		self.Nc = Nl*Np*Na*Nk #Number of cells
		self.dG = np.zeros((Nl,Np,Na,Nk))

		Scl = 1.0 # m*sqrt(2m)
		deg2rad = np.pi/180.0
		#Calculate dG, phase space volume for each cell
		#Assuming for now, uniform dimensions for all but K
		dx = self.dl*self.dk*(deg2rad*self.dp)*(deg2rad*self.da)

		for i in range(Nl):
			for j in range(Na):
				for k in range(Nk):
					L = self.Lc[i]
					A = self.Ac[j]
					K = self.Kc[k]
					dX = self.dl*(deg2rad*self.dp)*(deg2rad*self.da)*self.dk[k]

					self.dG[i,:,j,k] = L*np.sqrt(K)*np.sin(A*deg2rad)*dX
#Particle cloud
#Bunch of particles at same time
#Store relevant values for cloud in phase space
class pState(object):
	#Grab relevant particle values from an h5p file
	#Use Ts (timestep, not time) state
	def __init__(self,h5pF,Ts):

		#Find out how many particles we're dealing with
		self.T,self.pId = lfmpp.getH5pT(h5pF,"id",Ts)
		self.Np = len(self.pId)

		t,x = lfmpp.getH5pT(h5pF,"xeq",Ts)
		t,y = lfmpp.getH5pT(h5pF,"yeq",Ts)

		self.L = np.sqrt(x**2.0 + y**2.0)
		#Calculate phi in degrees in [0,360]
		pSgn = np.arctan2(y,x)*180.0/np.pi #[-180,180]
		#Remap
		Ind = pSgn<0
		pSgn[Ind] = pSgn[Ind] + 360

		self.phi = pSgn

		t,self.A = lfmpp.getH5pT(h5pF,"alpheq",Ts)
		t,self.K = lfmpp.getH5pT(h5pF,"keveq",Ts)
		t,self.Mu = lfmpp.getH5pT(h5pF,"mueq",Ts)

		Ind = np.isnan(self.Mu) | (self.Mu<0)
		self.Mu[Ind] = 0

		self.W = np.zeros(self.Np) #Room for weights
		self.isWgt = False #Weights not yet calculated/set

		self.F = [] #Holder for distribution function (t>0)

		self.isPDF = False

#Calculate weights for particle distribution relative to phase space discretization
def CalcWeights(pSt,pSpc):
	
	Np = pSt.Np
	Found = np.zeros(Np,dtype=bool)
	
	#Loop over unfound particles until everybody is weighted
	while not np.all(Found):
		#Find first unweighted particle
		N = Found.argmin()

		#Get phase space position of particle
		L = pSt.L[N]
		phi = pSt.phi[N]
		A = pSt.A[N]
		K = pSt.K[N]

		#Find cell of discretized phase space this particle is in
		#Hold as index vector (i,j,k,l) -> L_i,Phi_j,A_k,K_l
		iVec = locateCell(pSpc,(L,phi,A,K))

		#Find all particles in cell iVec
		inCell = locateP(pSt,pSpc,iVec)

		#Count cells in iVec
		NumIn = inCell.sum()

		#Evaluate distribution function at cell center of cell iVec
		fC = fDist(pSpc.Lc[iVec[0]],pSpc.Pc[iVec[1]],pSpc.Ac[iVec[2]],pSpc.Kc[iVec[3]])

		#Calculate weight, number of analytically-predicted (fC*dG) over number of actual
		#print(iVec,NumIn,fC)
		Wgt = fC*pSpc.dG[iVec]/NumIn

		#Now assign weight to all particles in cell iVec
		pSt.W[inCell] = Wgt
		Found[inCell] = True
		
		# print("Found %d now, %d total"%(NumIn.sum(),Found.sum()))
		if (NumIn <=0):
			print("Particle %d not found"%N)
			print("L,phi,A,K = %f,%f,%f,%f"%(L,phi,A,K))
			print("iVec = %s"%str(iVec))
			sys.exit()
	pSt.isWgt = True

#Given particle state and weights, calculate distribution function for a given phase space
#Calculate f(L,\phi,\alpha,K)
#And f(L,\Mu)

def calcPDF(pSt,pSpc,muMin=1,muMax=1.0e+5,Nmu=20,nOut=100):

	#Squash particle data to fit into phase space
	TINY = 1.0e-2 #Small relative to kev/L
	Ind = pSt.L < pSpc.Li[0]; pSt.L[Ind] = pSpc.Li[0]
	Ind = pSt.K < pSpc.Ki[0]; pSt.K[Ind] = pSpc.Ki[0]

	Ind = pSt.L > pSpc.Li[-1]; pSt.L[Ind] = pSpc.Li[-1] - TINY
	Ind = pSt.K > pSpc.Ki[-1]; pSt.K[Ind] = pSpc.Ki[-1] - TINY

	#Loop through all particles
	Np = pSt.Np
	Found = np.zeros(Np,dtype=bool)

	pSt.F = np.zeros(pSpc.dG.shape)
	pSt.Flm = np.zeros((pSpc.Nl,Nmu))

	dG_Mu = np.zeros(pSpc.dG.shape)
	n = 0
	while not np.all(Found):
		#Find first unweighted particle
		N = Found.argmin()

		#Get phase space position of particle
		L = pSt.L[N]
		phi = pSt.phi[N]
		A = pSt.A[N]
		K = pSt.K[N]

		#Find cell of discretized phase space this particle is in
		#Hold as index vector (i,j,k,l) -> L_i,Phi_j,A_k,K_l
		iVec = locateCell(pSpc,(L,phi,A,K))

		#Find all particles in cell iVec
		inCell = locateP(pSt,pSpc,iVec)

		NumIn = inCell.sum()
		#Total weight in cell iVec
		dW = pSt.W[inCell].sum()


		#Calculate characteristic Mu for cell iVec, use weighted average
		Mu = (pSt.W[inCell]*pSt.Mu[inCell]).sum()/dW
		dG_Mu[iVec] = Mu

		pSt.F[iVec] = dW/pSpc.dG[iVec]
		Found[inCell] = True

		if (n % nOut == 0):
			print("Iteration %d, %d particles localized."%(n,Found.sum()))	
		n = n+1
		
	#Fill L/Mu distribution function
	pSt.Lc = pSpc.Lc
	pSt.Li = pSpc.Li
	pSt.Mui = np.logspace(np.log10(muMin),np.log10(muMax),Nmu+1)
	pSt.Muc = 0.5*(pSt.Mui[0:-1] + pSt.Mui[1:])
	pSt.Nmu = Nmu

	for l in range(pSpc.Nl):
		for m in range(Nmu):
			#Find number of "real" particles with L,\Mu values in this cell
			Ind_L = (pSt.L >= pSt.Li[l]) & (pSt.L < pSt.Li[l+1])
			Ind_M = (pSt.Mu >= pSt.Mui[m]) & (pSt.Mu < pSt.Mui[m+1])
			inCell = Ind_L & Ind_M
			NumP = 0.0

			if (inCell.sum() > 0):
				#Number of particles is sum of weights of these particles
				NumP = pSt.W[inCell].sum()
	
			#Find phase space volume associated with L,Mu
			inVol = ( dG_Mu[l,:,:,:] >= pSt.Mui[m] ) & (dG_Mu[l,:,:,:] < pSt.Mui[m+1])
			
			
			if (inVol.sum() > 0):
				dG = pSpc.dG[l,inVol].sum()
				pSt.Flm[l,m] = NumP/dG	
			
	pSt.isPDF = True
#For position xVec = L,phi,alpha,K find which cell of pSpc it's in
def locateCell(pSpc,xVec):

	iVec = np.zeros(4,dtype=np.int)


	Ind_0 = (xVec[0] >= pSpc.Li[0:-1]) & (xVec[0] <= pSpc.Li[1:])
	Ind_1 = (xVec[1] >= pSpc.Pi[0:-1]) & (xVec[1] <= pSpc.Pi[1:])
	Ind_2 = (xVec[2] >= pSpc.Ai[0:-1]) & (xVec[2] <= pSpc.Ai[1:])
	Ind_3 = (xVec[3] >= pSpc.Ki[0:-1]) & (xVec[3] <= pSpc.Ki[1:])

	if (Ind_0.any()):
		iVec[0] = Ind_0.argmax()
	else:
		iVec[0] = -1

	if (Ind_1.any()):
		iVec[1] = Ind_1.argmax()
	else:
		iVec[1] = -1

	if (Ind_2.any()):
		iVec[2] = Ind_2.argmax()
	else:
		iVec[2] = -1

	if (Ind_3.any()):
		iVec[3] = Ind_3.argmax()
	else:
		iVec[3] = -1



	# print(iVec)
	if (iVec == -1).any():
		print("Particle not localized to phase space")
		print(xVec)
		print(iVec)
		sys.exit()
	return tuple(iVec)

#Find all particles from pSt in cell iVec of pSpc
def locateP(pSt,pSpc,iVec):
	
	inCell_L = (pSt.L >= pSpc.Li[iVec[0]]) & (pSt.L <= pSpc.Li[iVec[0]+1])
	inCell_P = (pSt.phi >= pSpc.Pi[iVec[1]]) & (pSt.phi<= pSpc.Pi[iVec[1]+1])
	inCell_A = (pSt.A >= pSpc.Ai[iVec[2]]) & (pSt.A <= pSpc.Ai[iVec[2]+1])
	inCell_K = (pSt.K >= pSpc.Ki[iVec[3]]) & (pSt.K <= pSpc.Ki[iVec[3]+1]) 

	inCell = inCell_L & inCell_P & inCell_A & inCell_K

	return inCell

def fDist(L,P,A,K,f0=1.0e+6,beta=5.2):
	fVal = f0*(K**(-beta))

	return fVal

#Get particle counts for L shell, all energy/phi/alpha
def shellCount(pSt,L0,dL):
	Indl = (pSt.L>L0) & (pSt.L<(L0+dL))

	Mul = pSt.Mu
	IndMu = (Mul>0) & (~np.isnan(Mul))
	Ind = Indl & IndMu

	Mul = pSt.Mu[Ind]

	Kl = pSt.K[Ind]
	Pl = pSt.phi[Ind]
	Al = pSt.A[Ind]
	Wl = pSt.W[Ind]
	Mul = pSt.Mu[Ind]
	return Wl,Kl,Mul

#Generates two panel figure of f(L,Mu)
#Ls = list of L shells to plot in top panel
def genDistPic(pSt,Ls=[7,9,11,13],dMin=1.0e-6,dMax=1.0,figSize=(10,10),figQ=300):

	LW = 1.5
	mLim = (10,2e+4)
	cbLab = "Density"
	Ls = np.array(Ls)
	Nlp = len(Ls)
	iLs = np.zeros(Nlp,dtype=int)
	LegS = []
	for i in range(Nlp):
		iLs[i] = np.abs(pSt.Lc-Ls[i]).argmin()
		lS = "L = %2.2f"%(pSt.Lc[iLs[i]])
		LegS.append(lS)

	cNorm = LogNorm(vmin=dMin,vmax=dMax)

	fig = plt.figure(figsize=figSize)#,tight_layout=True)
	gs = gridspec.GridSpec(3,1,height_ratios=[4,8,0.25])

	#Do 1D plots
	Ax = fig.add_subplot(gs[0,0])
	for i in range(Nlp):
		Ax = plt.loglog(pSt.Muc,pSt.Flm[iLs[i],:],label=LegS[i],linewidth=LW)
	plt.setp(plt.gca().get_xticklabels(),visible=False)
	plt.xlim(mLim)
	plt.legend(loc='lower left',fontsize="small")

	#Do 2D histogram
	Ax = fig.add_subplot(gs[1,0])
	pCol = Ax.pcolor(pSt.Mui,pSt.Li,pSt.Flm,norm=cNorm)
	plt.xscale('log')
	plt.xlabel('First Invariant [keV/nT]')
	plt.ylabel('L Shell')
	plt.xlim(mLim)

	#Do colorbar
	AxCbar = plt.subplot(gs[-1,:])
	plt.colorbar(pCol,cax=AxCbar,orientation='horizontal',label=cbLab)

	

