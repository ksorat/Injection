#Various routines to generate phase space densities from lfmtp runs

import numpy as np
import lfmPostproc as lfmpp
import sys
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
		self.dl = (Lmax-Lmin)/Nl

		self.Pi = np.linspace(0,360,Np+1)
		self.Pc = 0.5*(self.Pi[0:-1] + self.Pi[1:])
		self.Np = Np
		self.dp = (360-0)/Np

		self.Ai = np.linspace(0,180,Na+1)
		self.Ac = 0.5*(self.Ai[0:-1] + self.Ai[1:])
		self.Na = Na
		self.da = (180-0)/Na

		self.Ki = np.logspace(np.log10(Kmin),np.log10(Kmax),Nk+1)
		self.Kc = 0.5*(self.Ki[0:-1] + self.Ki[1:])
		self.Nk = Nk
		self.dk = self.Li[1:]-self.Li[0:-1]

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

		self.W = np.zeros(self.Np) #Room for weights
		self.isWgt = False #Weights not yet calculated/set

#Calculate weights for particle distribution relative to phase space discretization
def CalcWeights(pSt,pSpc):
	#For now assume identity function for PSD
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
		
		print("Found %d now, %d total"%(NumIn.sum(),Found.sum()))
		if (NumIn <=0):
			print("Particle %d not found"%N)
			print("L,phi,A,K = %f,%f,%f,%f"%(L,phi,A,K))
			print("iVec = %s"%str(iVec))
			sys.exit()
	pSt.isWgt = True

#For position xVec = L,phi,alpha,K find which cell of pSpc it's in
def locateCell(pSpc,xVec):

	iVec = np.zeros(4,dtype=np.int)
	iVec[0] = ((xVec[0] >= pSpc.Li[0:-1]) & (xVec[0] <= pSpc.Li[1:])).argmax()
	iVec[1] = ((xVec[1] >= pSpc.Pi[0:-1]) & (xVec[1] <= pSpc.Pi[1:])).argmax()
	iVec[2] = ((xVec[2] >= pSpc.Ai[0:-1]) & (xVec[2] <= pSpc.Ai[1:])).argmax()
	iVec[3] = ((xVec[3] >= pSpc.Ki[0:-1]) & (xVec[3] <= pSpc.Ki[1:])).argmax()

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