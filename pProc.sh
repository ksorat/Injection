#Combine files and move to destination
import sys
import os

spcs = ["p","o","hepp"]
Ks = [10,25,50]

RootDir = os.path.expanduser('~') + "/Work/Injection/"
H5pFin = RootDir + "Data/H5p/"
for s in spcs:
	for k in Ks:
		H5pDir = RootDir + s + "Inj" + "%02d"%k
		print("Collecting from %s"%H5pDir)
		os.system("h5pcat.py %s/*.h5part"%H5pDir)
		print("Moving to %s"%H5pFin)
		os.system("mv %s/*All*.h5part %s"%(H5pDir,H5pFin))

