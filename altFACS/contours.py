import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import gaussian_kde as kde
from matplotlib.colors import Normalize
from matplotlib import cm
from matplotlib.patches import Polygon
from matplotlib import path

from altFACS.density import *
        
def getContours(data: pd.DataFrame, x='FSC-A', y='SSC-A', **kwargs)->plt.Polygon:
    '''function to generate and return a contour polygon for gating'''
    
    x = data[x]
    y = data[y]
    
    #Get **kwargs
    contour    = kwargs.get('contour', 2)
    population = kwargs.get('population', 0) #which population for plots with more than one
    nbins      = kwargs.get('densityScatterPlot_bins_number', 300)
    
    # Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
    k = kde([x,y])
    xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    
    CS = plt.contour(xi, yi, zi.reshape(xi.shape));
    
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
    poly = Polygon(np.column_stack([xp, yp]), fill=False)
    
    return poly


def contourPlot(data: pd.DataFrame, x: str, y: str, poly: plt.Polygon, **kwargs):
    
    #Get **kwargs
    title     = kwargs.get('title', 'contourPlot_figure')
    ringcolor = kwargs.get('contour_ring_color', 'magenta')
    save      = kwargs.get('save', False)
    savepath  = kwargs.get('savepath', './')
    polyfill  = kwargs.get('polygon_fill', False)
    
    #Set plot kwarg to True
    kwargs['plot'] = True
    #Set save kwarg to False
    kwargs['save'] = False

    densityScatterPlot(data, 'FSC-A', 'SSC-A', **kwargs);
   
    #Define polygon
    poly = Polygon(poly.xy, edgecolor = ringcolor, fill=polyfill)
    
    plt.gca().add_patch(poly);
    
    if save:
        plt.savefig(savepath+title)
        
    
def scatterGate(data: pd.DataFrame, poly: plt.Polygon, **kwargs)->pd.DataFrame:
    '''Add boolean Scatter Gates indicating events within the input polygon.'''
    
    assert 'FSC-A' in data.columns
    assert 'SSC-A' in data.columns
    
    #Get **kwargs
    verbose     = kwargs.get('verbose', True)
    
    ##get data coordinates
    coords = np.array(data[['FSC-A', 'SSC-A']])

    ##get polygon coordinates
    p = path.Path(poly.get_xy())

    #Detect gated events
    data.loc[:, "Scatter+"] = p.contains_points(coords)
    scatter = data[data['Scatter+']].copy()
    
    ##Count scatter_gated_events
    scatter_gated_events = len(scatter)
    
    if verbose:
        print('Scatter gated events =',scatter_gated_events) 
    
    return data