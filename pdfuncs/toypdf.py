import numpy as np
import lfmPSD as lpsd

pSpc = lpsd.PhaseSpace(4,10,10,20,20,10,500,10)

p0 = lpsd.pState("bigtoy.h5part",0)

lpsd.CalcWeights(p0,pSpc)