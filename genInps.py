#Generate Input decks for various simulations associated with our injection project

import lxml.etree as et
import numpy as np
import os

def writeInpXML(spc,K0,rad,phi,psi,alpha,T0=1750.0,Tfin=2250,iMeth="fp",dt=0.1,dtS=1.0,dtF=1.0,outDir="Data",tagS="pDat"):
	iDeck = et.Element('Params')

	#Particle details
	pInfo = et.SubElement(iDeck,"particle")
	pInfo.set("species",spc)
	pInfo.set("K0",str(K0))

	#Phase space dimensions
	addDim(iDeck,"radius",rad)
	addDim(iDeck,"phi",phi)
	addDim(iDeck,"psi",psi)
	addDim(iDeck,"alpha",alpha)

	#Time details
	Ns = np.int(dtS/dt)
	Nf = np.int(dtF/dt)

	tInfo = et.SubElement(iDeck,"time")
	tInfo.set("T0",str(T0))
	tInfo.set("tfin",str(Tfin))
	tInfo.set("Ns",str(Ns))
	tInfo.set("Nf",str(Nf))

	#Integrator details
	intInfo = et.SubElement(iDeck,"integrator")
	intInfo.set("dt",str(dt))
	intInfo.set("method",iMeth)

	#Assuming field details
	fldInfo = et.SubElement(iDeck,"field")
	fldInfo.set("infile","ebtab.txt")

	#Output info
	outInfo = et.SubElement(iDeck,"output")
	outInfo.set("outdir",outDir)
	outInfo.set("mu","T")
	outInfo.set("work","F")
	outInfo.set("trace","F")

	#Run tag
	runInfo = et.SubElement(iDeck,"run")
	runInfo.set("tag",tagS)

	inpTree = et.ElementTree(iDeck)
	return inpTree

def addDim(iDeck,LabS,dom):
	dimInfo = et.SubElement(iDeck,LabS)
	dimInfo.set("min",str(dom[0]) )
	dimInfo.set("max",str(dom[1]) )
	dimInfo.set("N",  str(dom[2]) )

#Adds stream info to input deck (that has been turned into XML tree)
def addStream(iTree,Ts0=0,Tsfin=1,sfrac=0.5):
	iDeck = iTree.getroot()
	sInfo = et.SubElement(iDeck,"stream")
	sInfo.set("active","T")
	sInfo.set("Ts0",str(Ts0))
	sInfo.set("Tsfin",str(Tsfin))
	sInfo.set("sfrac",str(sfrac))

	inpTree = et.ElementTree(iDeck)
	return inpTree

#Generate batch script to run all the input decks just generated
def genRunner(ComS,batchCom="lfmtpBatch.sh",fRunner="SubAll.sh"):
	N = len(ComS)
	with open(fRunner,"w") as fId:
		fId.write("#!/bin/bash")
		fId.write("\n\n")
		for n in range(N):
			outS = batchCom + " " + ComS[n] + "\n"
			fId.write(outS)

		fId.write("\n")
	os.system("chmod u+x %s"%(fRunner))

SimComS = []

gen_sInj = False #Single injection front
gen_mInj = False #Multiple injection long run
gen_csInj = False #Single injection, cold particles
gen_psInj = True #Single injection, log-spaced energies

gen_Run = True

#Single injection runs
#Spcs = ["p","O","Hepp"]
#K0s = [10,50,100]
Spcs = ["Hepp"]
K0s = [10]

rad = [10,12.2,100]
phi = [157.5,170,50]
psi = [0,360,1]
alpha = [20,90,10]
time = [1750.0,2250.0]
iOpts = [0.1,"fp"]
dtOuts = [1.0,1.0]
outDir = "sInj"

if (gen_sInj):
	#Generate input decks for single injection sims
	print("Writing single injection input decks, Np=%d"%(rad[2]*phi[2]*psi[2]*alpha[2]))
	T0 = time[0]
	Tfin = time[1]
	dt = iOpts[0]

	Ns = len(Spcs)
	Nk = len(K0s)
	for n in range(Ns):
		for k in range(Nk):
			#Create input deck
			spc = Spcs[n]
			K = K0s[k]
			
			tagS = spc + "_" + outDir + ".K" + str(np.int(K))
			fXML = "Inps/" + tagS + ".xml"
			print("Writing input deck for %s"%tagS)
			inpTree = writeInpXML(spc,K,rad,phi,psi,alpha,T0=T0,Tfin=Tfin,dt=dt,dtS=dtOuts[0],dtF=dtOuts[1],outDir=outDir,tagS=tagS)
			inpTree.write(fXML,pretty_print=True)

			#Command to add to batch script
			ComS = fXML + " 1 1"
			SimComS.append(ComS)
#Single injection, cold (1k particles)
Spcs = ["p","O","Hep","Hepp"]
K0s = [0.001]

rad = [10,12.2,10]
phi = [157.5,170,10]
psi = [0,360,1]
alpha = [20,90,10]
time = [1750.0,2250.0]
iOpts = [0.1,"fp"]
dtOuts = [1.0,1.0]
outDir = "csInj"
if (gen_csInj):
	#Generate input decks for single injection sims
	print("Writing single injection (cold) input decks, Np=%d"%(rad[2]*phi[2]*psi[2]*alpha[2]))
	T0 = time[0]
	Tfin = time[1]
	dt = iOpts[0]

	Ns = len(Spcs)
	Nk = len(K0s)
	for n in range(Ns):
		for k in range(Nk):
			#Create input deck
			spc = Spcs[n]
			K = K0s[k]
			
			tagS = spc + "_" + outDir + ".K" + str(np.int(K))
			fXML = "Inps/" + tagS + ".xml"
			print("Writing input deck for %s"%tagS)
			inpTree = writeInpXML(spc,K,rad,phi,psi,alpha,T0=T0,Tfin=Tfin,dt=dt,dtS=dtOuts[0],dtF=dtOuts[1],outDir=outDir,tagS=tagS)
			inpTree.write(fXML,pretty_print=True)

			#Command to add to batch script
			ComS = fXML + " 1 1"
			SimComS.append(ComS)

#Multiple injection runs
Nb = 10
bId = 0 #Block ID, use to guarantee contiguous IDs

Nk = 8 #Number of log-spaced energy bins
#Spcs = ["p"]
#Spcs = ["O"]
Spcs = ["Hepp"]
K0s = np.round(np.logspace(1,2,Nk)/5)*5
rad = [10,12.5,50]
phi = [135,225,50]
psi = [0,360,1]
alpha = [20,90,8]
time = [1750,4500]
tStr = [1750,4250]
iOpts = [0.1,"fp"]
dtOuts = [10.0,10.0]
sF = 0.75
outDir = "mInj"

print("\n")

if (gen_mInj):
	print("Writing multiple injection input decks, Np=%d"%(rad[2]*phi[2]*psi[2]*alpha[2]))

	#Generate input decks for multiple injection sims
	T0 = time[0]
	Tfin = time[1]
	dt = iOpts[0]

	Ns = len(Spcs)
	Nk = len(K0s)

	for n in range(Ns):
		for b in range(Nb):	
			rId = 1 + (bId+b)*Nk
			for k in range(Nk):
				#Create input deck
				spc = Spcs[n]
				K = K0s[k]
				#Tag needs run id to avoid overwriting with multiple blocks
				tagS = spc + "_" + outDir + ".K" + str(np.int(K)) + ".r" + str(rId)
	
				fXML = "Inps/" + tagS + ".xml"
				print("Writing input deck for %s"%tagS)
				inpTree = writeInpXML(spc,K,rad,phi,psi,alpha,T0=T0,Tfin=Tfin,dt=dt,dtS=dtOuts[0],dtF=dtOuts[1],outDir=outDir,tagS=tagS)
				inpTree = addStream(inpTree,Ts0=tStr[0],Tsfin=tStr[1],sfrac=sF)
				inpTree.write(fXML,pretty_print=True)
	
				#Command to add to batch script
				ComS = fXML + " %d %d"%(rId,rId)
				SimComS.append(ComS)
	
				rId = rId+1


#Single injection, log-spaced energies
Nb = 10
bId = 0 #Block ID, use to guarantee contiguous IDs

Nk = 10 #Number of log-spaced energy bins
Ki = np.log10(5)
Kf = np.log10(200)
Spcs = ["p","O","Hep","Hepp"]

K0s = np.round(np.logspace(Ki,Kf,Nk)/5)*5

rad = [10,12.2,100]
phi = [157.5,170,50]
psi = [0,360,1]
alpha = [20,90,10]
time = [1750.0,2100.0]
iOpts = [0.1,"fp"]
dtOuts = [1.0,1.0]

outDir = "psInj"

print("\n")

if (gen_psInj):
	print("Writing single injection (PDFs) input decks, Np=%d"%(rad[2]*phi[2]*psi[2]*alpha[2]))

	#Generate input decks for single injection sims
	T0 = time[0]
	Tfin = time[1]
	dt = iOpts[0]

	Ns = len(Spcs)
	Nk = len(K0s)

	for n in range(Ns):
		for b in range(Nb):	
			rId = 1 + (bId+b)*Nk
			for k in range(Nk):
				#Create input deck
				spc = Spcs[n]
				K = K0s[k]
				#Tag needs run id to avoid overwriting with multiple blocks
				tagS = spc + "_" + outDir + ".K" + str(np.int(K)) + ".r" + str(rId)
	
				fXML = "Inps/" + tagS + ".xml"
				print("Writing input deck for %s"%tagS)
				inpTree = writeInpXML(spc,K,rad,phi,psi,alpha,T0=T0,Tfin=Tfin,dt=dt,dtS=dtOuts[0],dtF=dtOuts[1],outDir=outDir,tagS=tagS)
				inpTree.write(fXML,pretty_print=True)
	
				#Command to add to batch script
				ComS = fXML + " %d %d"%(rId,rId)
				SimComS.append(ComS)
	
				rId = rId+1

if (gen_Run):
	print("\nWriting run script")
	genRunner(SimComS)


