import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import gaussian_kde as kde
from matplotlib.colors import Normalize
from matplotlib import cm
from matplotlib.patches import Polygon
from matplotlib import path
        
def getContours(x, y, contour: int, **kwargs)->plt.Polygon:
    '''function to generate and return a contour polygon for gating'''
    
    #Get **kwargs
    nbins     = kwargs.get('nbins', 300)
    plot      = kwargs.get('plot', False)
    title     = kwargs.get('title', 'contourPlot_figure')
    edgecolor = kwargs.get('edgecolor', 'magenta')
    save      = kwargs.get('save', False)
    
    # Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
    k = kde([x,y])
    xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    
    if plot==False:
        plt.ioff()
    
    CS = plt.contour(xi, yi, zi.reshape(xi.shape));
    
    if save:
        fig.savefig(title)
    
    if plot==False:
        plt.close()
    else:
        plt.show()

    #Extract desired contour
    coords = CS.allsegs[contour][0]
    
    #Convert to a list
    coord_list=list()
    for point in coords:
        coord_list.append([point[0], point[1]])
    coord_list

    #Convert to an array
    coord_array = np.array(coord_list)

    #Pull out coordinates
    xp = coord_array.T[0]
    yp = coord_array.T[1]

    #Define polygon
    poly = Polygon(np.column_stack([xp, yp]), edgecolor="magenta", fill=False)
    
    return poly