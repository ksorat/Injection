#Generate input decks for single injection, multiple energy sweep
import lfmPreproc as lfmpre
import os

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


#Each run is 10^5 particles, run 10 blocks

Spcs = ["p","O","Hep","Hepp"]
Nb = 10
b0 = 0 #Block offset

oDir = "finInj"

K0 = [5,200,25]
rad = [10,12.2,16]
phi = [157.5,170,10]
psi = [0,360,1]
alpha = [20,160,25]

T0 = 1750.0
Tf = 4450.0 #45 minutes

dt = 1.0

Ns = len(Spcs)

SimS = [] #Run strings

#Generate input deck for each species
for n in range(Ns):
	oTag = "%sInj"%(Spcs[n])
	idF = "Inps/%sInj.xml"%(Spcs[n])

	iDeck = lfmpre.genDeck(spc=Spcs[n],tagStr=oTag,outDir=oDir)
	iDeck = lfmpre.dimsDeck(iDeck,K=K0,R=rad,P=phi,A=alpha,psi=psi)
	iDeck = lfmpre.itDeck(iDeck,T0=T0,Tf=Tf,dt=dt,dtS=10,dtF=10,iMeth="fp")
	lfmpre.writeDeck(iDeck,fOut=idF)

	ComS = idF + " %d %d"%(b0+1,b0+Nb)
	SimS.append(ComS)

print("\nWriting run script")
genRunner(SimS)
