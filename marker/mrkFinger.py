#Given phi/radial range, marks the point to setup injection

import numpy as np
import os
from visit import *
from visit_utils import *
from visit_utils.common import lsearch #lsearch(dir(),"blah")
import lfmGrids as lfm
import pyVisit as pyv

Quiet = True
T0 = 1750

Phi0s = [157.5,135]
Phi1s = [170,185]
R0s = [10,9]
R1s = [12.2,13]
Cols = [(0, 255, 255, 255),(0,0,255,255)]
#EqSlc DB
EqDir = os.path.expanduser('~') + "/Work/Injection/Data/eqSlc_sInj"
Src0 = EqDir + "/eqSlc.*.vti database"

#dBz
abBz = 25;
dBzBds = [-abBz,abBz]

if (Quiet):
	LaunchNowin()
else:
	Launch()

#Do some defaults
pyv.lfmExprs()

#Open databases
OpenDatabase(Src0)
md0 = GetMetaData(Src0)

#Get time
Time = np.array(md0.times)
Nt = np.argmax(Time>=T0)



DefineScalarExpression("PCut","Phi*RCut0*RCut1")
DefineScalarExpression("RCut","Rcyl*PCut0*PCut1")

#Draw field marker
pyv.lfmPCol(Src0,"dBz",vBds=dBzBds,pcOpac=0.7,Inv=True)

#Draw wedges
Nw = len(Phi0s)
for n in range(Nw):
	DefineScalarExpression("RCut0_%d","if( ge(Rcyl, %f), 1, 0)"%(n,R0s[n])) 
	DefineScalarExpression("RCut1_%d","if( le(Rcyl, %f), 1, 0)"%(n,R1s[n])) 
	DefineScalarExpression("PCut0_%d","if( ge(Phi, %f), 1, 0)"%(n,Phi0s[n])) 
	DefineScalarExpression("PCut1_%d","if( le(Phi, %f), 1, 0)"%(n,Phi1s[n])) 
	DefineScalarExpression("Wedge_%d","RCut0*RCut1*PCut0*PCut1"%(n))

	AddPlot("Contour","Wedge_%d"(n))
	cOp = GetPlotOptions()
	cOp.contourMethod = 1
	#cOp.contourValue = tuple([Phi0,Phi1])
	cOp.contourValue = 1
	cOp.colorType = 0
	cOp.singleColor = Cols[n]
	cOp.legendFlag=0
	cOp.lineWidth=2
	print(cOp)
	SetPlotOptions(cOp)

SetTimeSliderState(Nt)
DrawPlots()
SaveWindow()