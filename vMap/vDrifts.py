import sys
import os
import numpy as np
import datetime
from visit import *
from visit_utils import *
from visit_utils.common import lsearch #lsearch(dir(),"blah")
import pyVisit as pyv

RootDir = os.path.expanduser('~') + "/Work/Injection/VTIs/"
fldSlc = RootDir + "/SNS-Bz-5-Vx400-N5-F200_mhd_1141000.vti"

#fldSlc = "testSlc.vti"
Quiet = True
if (Quiet):
	LaunchNowin()
else:
	Launch()

OpenDatabase(fldSlc)

#Do some defaults
pyv.lfmExprsEB()
pyv.setAtts()

md0 = GetMetaData(fldSlc)

#ExB velocity (in km/s)
#DefineScalarExpression("Veb","1000*Emag/Bmag")

DefineScalarExpression("Veb","if ( ge(Bmag,1.0e-6), 1000*Emag/Bmag, 0)")
#BxGrad (in 1/Re, convert to 1/km)
DefineScalarExpression("BxGB","magnitude(cross(Bfld,gradient(Bmag)))/(Bmag*Bmag*6380.0)")

#Non-energy part of Vd
q = 1.6021766e-19 #Coulombs
#Will calculate drift velocity (m/s per Joule, want km/s per kev)
Scl = (1.0e+6)/( q*6.242e+15*1.0e+3)
#Drift velocity (km/s per Joule)
DefineScalarExpression("VDpN","1.0e+6*BxGB/(%f*Bmag)"%(q))
DefineScalarExpression("VdPkev","%f*BxGB/Bmag"%(Scl))

#Equality energy (in kev), 2/3 from assuming alpha=45o
DefineScalarExpression("eqKevA","(2/3.0)*Veb/VdPkev")
DefineScalarExpression("eqKev","if( ge(RadAll,2.0), eqKevA,0.0)")
#Create slice of eqKev

pyv.lfmPCol(fldSlc,"eqKev",cMap="hot_desaturated",vBds=[1,750],Log=True)

AddOperator("Slice",0)
slOp = GetOperatorOptions(0)
slOp.axisType = 2
SetOperatorOptions(slOp,0)

AddOperator("Threshold",1)
tOp = GetOperatorOptions(1)
tOp.listedVarNames = ("RadAll")
tOp.lowerBounds = (2)
SetOperatorOptions(tOp,1)

pyv.cleanLegends([0.025],[0.9],["Particle Energy (keV)\nDrift/ExB Equality"])
DrawPlots()

SaveWindow()
