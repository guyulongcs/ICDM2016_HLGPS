__author__ = 'guyulong'

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from Config import *

def loadDataVenue():
    fileStatisVenue = Config.folderData + Config.folderDataParsed + Config.fileAnalyseVenue
    file = fileStatisVenue
    (x,y,z)=np.loadtxt(file,unpack=True)
    return (x,y,z)


def randrange(n, vmin, vmax):
    return (vmax-vmin)*np.random.rand(n) + vmin





def plotVenue(x,y,z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    c='r'
    m='o'

    for i in range(0,len(x)):
        xs = x[i]
        ys = y[i]
        zs = z[i]
        ax.scatter(xs, ys, zs, c=c, marker=m)

    ax.set_xlabel('latitude')
    ax.set_ylabel('longitude')
    ax.set_zlabel('count')
    ax.set_title("Count of venue over latitude and longitude")

    plt.show()





def plot2(x,y,z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    for i in range(0,len(x)):
        xs = x[i]
        ys = y[i]
        zs = z[i]
        ax.bar(xs, ys, zs, zdir='y', color='r', alpha=0.8)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')


    plt.show()


def __main__():
    x,y,z=loadDataVenue()
    plotVenue(x,y,z)
    #plot2()


__main__()
