
import sys
import math
import numpy as np
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt

deg2rad = math.pi/180.0

def getSliceData(filename,i,slicename,varname,flipaxes):
    words = slicename.split('_')

    with h5py.File(filename,'r') as hf:

        c1 = hf.get('C'+words[0]).value
        c2 = hf.get('C'+words[1]).value
        d = hf.get('Step#' + str(i) + '/' + varname).value

        if flipaxes:
            temp = c1
            c1 = c2
            c2 = temp
            d = np.transpose(d)
            temp = words[0]
            words[0] = words[1]
            words[1] = temp

        if words[1] == 'phi':
            c2 = c2*3.1415/180.0
            c2 = np.hstack((c2,c2[0]))
            d = np.vstack((d,d[0,:]))

        x, y = np.meshgrid(c1, c2)

        if words[1] == 'phi':
            x, y = x*np.cos(y), x*np.sin(y)

    return x,y,d

def getVelDist(h5path,i,varname,rel):

    with h5py.File(h5path,'r') as hf:

        # TODO convert k to velocity magnitude

        Ck = hf.get('Ck').value
        Calpha = hf.get('Calpha').value
        Cpsi = hf.get('Cpsi').value
        Dk = hf.get('Dk').value
        Dalpha = hf.get('Dalpha').value
        Dpsi = hf.get('Dpsi').value
        Ik = hf.get('Ik').value
        Ialpha = hf.get('Ialpha').value

        pdist = hf.get('Step#' + str(i) + '/' + varname).value
        dV = getPsiDV(Ck, Calpha, Cpsi, Dk, Dalpha, Dpsi, rel)
        kalpha = np.sum(pdist*dV, axis=(0))

        x, y = np.meshgrid(np.log10(Ik), Ialpha*deg2rad)
        x, y = x*np.cos(y), x*np.sin(y)

        return x,y,kalpha

def getCellKHist(filename,steps,varname,rel):

    with h5py.File(filename,'r') as hf:

        m0 = hf.attrs['m0']
        Ck = hf.get('Ck').value
        Calpha = hf.get('Calpha').value
        Cpsi = hf.get('Cpsi').value
        Dk = hf.get('Dk').value
        Dalpha = hf.get('Dalpha').value
        Dpsi = hf.get('Dpsi').value

        khist = np.empty([len(Ck),0])
        times = np.empty(0)
        for s in steps:

            group = hf.get('Step#' + str(s))
            t = group.attrs['time']
            times = np.hstack((times, t))

            pdist = hf.get('Step#' + str(s) + '/' + varname).value
            dV = getAlphaPsiDV(Ck, Calpha, Cpsi, Dk, Dalpha, Dpsi, rel)

            k = np.sum(pdist*dV, axis=(0,1))
            k = np.reshape(k, (np.size(Ck),1) )
            khist = np.hstack((khist, k))

        x,y = np.meshgrid(times,Ck)

    return x,y,khist

def getAlphaPsiDV(Ck ,Calpha, Cpsi, Dk, Dalpha, Dpsi, rel):
    m0 = 1.0
    dV = np.zeros((Cpsi.size,Calpha.size,Ck.size), dtype=float)
    for ipsi in range(Cpsi.size):
        for ialpha in range(Calpha.size):
            for ik in range(Ck.size):
                if rel: # relativisitc
                    print 'Error: relativistic option not implemented yet'
                    sys.exit()
                else:
                    kScl = math.sqrt(2*m0*Ck[ik])
                    sA = math.sin(deg2rad*Calpha[ialpha])
                    dV[ipsi,ialpha,ik] = kScl*deg2rad*Dalpha[ialpha] * sA*kScl*(deg2rad*Dpsi[ipsi])
    return dV

def getPsiDV(Ck ,Calpha, Cpsi, Dk, Dalpha, Dpsi, rel):
    m0 = 1.0
    dV = np.zeros((Cpsi.size,Calpha.size,Ck.size), dtype=float)
    for ipsi in range(Cpsi.size):
        for ialpha in range(Calpha.size):
            for ik in range(Ck.size):
                if rel: # relativisitc
                    print 'Error: relativistic option not implemented yet'
                    sys.exit()
                else:
                    kScl = math.sqrt(2*m0*Ck[ik])
                    sA = math.sin(deg2rad*Calpha[ialpha])
                    dV[ipsi,ialpha,ik] = sA*kScl*(deg2rad*Dpsi[ipsi])
    return dV
