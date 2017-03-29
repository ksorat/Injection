
import lxml.etree as et

def addPop(el, idx, files, weighting, seriesfile=None, n0=None, kT0=None):
    pop = et.SubElement(el,"population"+str(idx))
    pop.set("files",files)
    pop.set("weighting",weighting)
    if seriesfile is not None:
        pop.set("seriesfile",seriesfile)
    if n0 is not None:
        pop.set("n0",n0)
    if kT0 is not None:
        pop.set("kT0",kT0)

def addDim(el, LabS, dom, log=None):
    dimInfo = et.SubElement(el,LabS)
    if len(dom) == 3:
        dimInfo.set("N",  str(dom[2]) )
        dimInfo.set("min",str(dom[0]) )
        dimInfo.set("max",str(dom[1]) )
    elif len(dom) == 2:
        dimInfo.set("min",str(dom[0]) )
        dimInfo.set("max",str(dom[1]) )
    elif len(dom) == 1:
        dimInfo.set("N",  str(dom[0]) )
    if log is not None:
        dimInfo.set("log",log)

def addAllDims(el, log="T", r=[2.1,20,200], theta=[7], phi=[301], k=[1,1000,100], alpha=[30], psi=[1]):
    #Phase space dimensions
    addDim(el,"r",r)
    addDim(el,"theta",theta)
    addDim(el,"phi",phi)
    addDim(el,"k",k,log=log)
    addDim(el,"alpha",alpha)
    addDim(el,"psi",psi)

def addSlice2D(el, idx, dim1, dim2):
    slc = et.SubElement(el,"slice2D"+str(idx))
    slc.set("dim1",dim1)
    slc.set("dim2",dim2)
    return slc

def addSlice3D(el, idx, dim1, dim2, dim3):
    slc = et.SubElement(el,"slice3D"+str(idx))
    slc.set("dim1",dim1)
    slc.set("dim2",dim2)
    slc.set("dim3",dim3)
    return slc

def addCell(el, idx, r, phi, theta):
    cell = et.SubElement(el,"cell"+str(idx))
    cell.set("r",str(r))
    cell.set("phi",str(phi))
    cell.set("theta",str(theta))

iDeck = et.Element('Params')

el = et.SubElement(iDeck,"particles")
el.set("species","")
el.set("equatorial","F")

addPop(el, 1, "~skareem/Work/Injection/Data/pInj*.h5part", "maxNTSeries", seriesfile="maxwellSeries.txt")
addPop(el, 2, "~skareem/Work/Injection/Data/pInj*.h5part2", "maxNTSeries2", seriesfile="maxwellSeries.txt2")

el = et.SubElement(iDeck,"timing")
el.set("weighting","1750")
el.set("calculation","1750:500:4450")

el = et.SubElement(iDeck,"options")
el.set("background","T")
el.set("relativistic","F")

el = et.SubElement(iDeck,"phasespace")
addAllDims(el)

el = et.SubElement(iDeck,"output")
el.set("base","out")
el.set("fullevery","0")

slc = addSlice2D(el,1,"r","phi")
addDim(slc,"r",[-1,1])
slc = addSlice3D(el,1,"r","theta","phi")
addDim(slc,"k",[-1,1])
addCell(el,1,7,120,90)

inpTree = et.ElementTree(iDeck)

filename = "test.xml"
inpTree.write(filename,pretty_print=True)
