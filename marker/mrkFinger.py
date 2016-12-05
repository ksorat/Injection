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

Phi0s = [157.5,150]
Phi1s = [170,177.5]
R0s = [10,9.0]
R1s = [12.2,13.5]
Cols = [(0, 255, 255, 255),(0,0,255,255),(255,0,255,255)]
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
	DefineScalarExpression("RCut0_%d"%(n),"if( ge(Rcyl, %f), 1, 0)"%(R0s[n])) 
	DefineScalarExpression("RCut1_%d"%(n),"if( le(Rcyl, %f), 1, 0)"%(R1s[n])) 
	DefineScalarExpression("PCut0_%d"%(n),"if( ge(Phi, %f), 1, 0)"%(Phi0s[n])) 
	DefineScalarExpression("PCut1_%d"%(n),"if( le(Phi, %f), 1, 0)"%(Phi1s[n])) 
	DefineScalarExpression("Wedge_%d"%(n),"RCut0_%d*RCut1_%d*PCut0_%d*PCut1_%d"%(n,n,n,n))

	AddPlot("Contour","Wedge_%d"%(n))
	cOp = GetPlotOptions()
	cOp.contourMethod = 1
	#cOp.contourValue = tuple([Phi0,Phi1])
	cOp.contourValue = 1
	cOp.colorType = 0
	cOp.singleColor = Cols[n]
	cOp.legendFlag=0
	cOp.lineWidth=2
	
	SetPlotOptions(cOp)

SetTimeSliderState(Nt)
DrawPlots()
SaveWindow()