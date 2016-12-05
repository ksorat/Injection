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
DefineScalarExpression("Veb","1000*Emag/Bmag")

#BxGrad (in 1/Re, convert to 1/km)
DefineScalarExpression("BxGB","cross(Bfld,grad(Bfld))/(Bmag*Bmag*6380.0)")

#Non-energy part of Vd
q = 1.6021766e-19 #Coulombs
#Will calculate drift velocity (m/s per Joule, want km/s per kev)
Scl = (1.0e+6)/( q*6.242e+15*1.0e+3)
#Drift velocity (km/s per Joule)
DefineScalarExpression("VDpN","1.0e+6*BxGB/(%f*Bmag)"%(q))
DefineScalarExpression("VdPkev","%f*BxGB/Bmag"%(Scl))

#Equality energy (in kev)
DefineScalarExpression("eqKev","Veb/VdPkev")

#Create slice of eqKev
AddPlot("Pseudocolor","eqKev")
AddOperator("Slice",0)