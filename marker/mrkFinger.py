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
Phi0 = 157.5
Phi1 = 170
R0 = 10
R1 = 12.2

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

DefineScalarExpression("RCut0","if( ge(Rcyl, %f), 1, 0)"%(R0)) 
DefineScalarExpression("RCut1","if( le(Rcyl, %f), 1, 0)"%(R1)) 
DefineScalarExpression("PCut0","if( ge(Phi, %f), 1, 0)"%(Phi0)) 
DefineScalarExpression("PCut1","if( le(Phi, %f), 1, 0)"%(Phi1)) 

DefineScalarExpression("PCut","Phi*RCut0*RCut1")
DefineScalarExpression("RCut","Rcyl*PCut0*PCut1")

DefineScalarExpression("Wedge","RCut0*RCut1*PCut0*PCut1")
#Draw field marker
pyv.lfmPCol(Src0,"dBz",vBds=dBzBds,pcOpac=0.7,Inv=True)

#Draw wedge
AddPlot("Contour","Wedge")
cOp = GetPlotOptions()
cOp.contourMethod = 1
#cOp.contourValue = tuple([Phi0,Phi1])
cOp.contourValue = 1
cOp.colorType = 0
cOp.singleColor = (0, 255, 255, 255)
cOp.legendFlag=0
cOp.lineWidth=2
SetPlotOptions(cOp)

SetTimeSliderState(Nt)
DrawPlots()
SaveWindow()