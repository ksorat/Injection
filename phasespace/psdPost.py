
import sys
import numpy as np
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt

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

def getVelDist(h5path,i,varname):

    with h5py.File(h5path,'r') as hf:

        Ck = hf.get('Ck').value # TODO convert k to velocity magnitude
        Calpha = hf.get('Calpha').value*3.1415/180.0
        d = hf.get('Step#' + str(i) + '/' + varname).value
        x, y = np.meshgrid(Ck, Calpha)
        x, y = x*np.cos(y), x*np.sin(y)
        return x,y,d

def getCellKHist(filename,steps,varname):

    with h5py.File(filename,'r') as hf:

        Ck = hf.get('Ck').value
        Calpha = hf.get('Calpha').value

        khist = np.empty([len(Ck),0])
        times = np.empty(0)
        for s in steps:
            group = hf.get('Step#' + str(s))
            t = group.attrs['time']
            times = np.hstack((times, t))
            alpha = hf.get('Step#' + str(s) + '/' + varname).value
            k = alpha.squeeze()
            # kalpha = hf.get('Step#' + str(s) + '/' + varname).value
            # kalpha = kalpha * np.reshape(np.sin(Calpha*3.1415/180.0), (np.size(Calpha),1) )
            k = np.reshape(k, (np.size(Ck),1) )
            khist = np.hstack((khist, k))

        x,y = np.meshgrid(times,Ck)

    return x,y,khist