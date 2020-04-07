import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import gaussian_kde as kde
from matplotlib.colors import Normalize
from matplotlib import cm

def densityScatterPlot(data: pd.DataFrame, x_channel: str, y_channel: str, **kwargs):
    '''function to generate publication quality 2D-density plots from FACS data'''
    
    #Get **kwargs
    plot      = kwargs.get('plot', True)
    title     = kwargs.get('title', 'densityScatter_figure')
    xlabel    = kwargs.get('xlabel', x_channel)
    ylabel    = kwargs.get('ylabel', y_channel)
    cmap      = kwargs.get('cmap', 'jet')
    size      = kwargs.get('size', 1)
    save      = kwargs.get('save', False)
    savepath  = kwargs.get('savepath', './')
    
    x = data[x_channel]
    y = data[y_channel]
    
    #Calculate density
    densObj = kde( [x, y] )

    vals = densObj.evaluate( [x, y] )

    colours = np.zeros( (len( vals ),3) )
    norm = Normalize( vmin=vals.min(), vmax=vals.max() )

    #Can put any colormap you like here.
    colours = [cm.ScalarMappable( norm=norm, cmap=cmap).to_rgba( val ) for val in vals]
    
    if plot:
        plt.scatter( x, y, color=colours, s=size)
        plt.xlabel(xlabel);
        plt.ylabel(ylabel);
        #plt.show()
    else:
        plt.ioff()
        plt.scatter( x, y, color=colours, s=size)
        plt.xlabel(xlabel);
        plt.ylabel(ylabel);
        
    if save:
        plt.tight_layout()
        plt.savefig(savepath+title)
        
    if plot==False:
        plt.close()
        
    #Restore interactive plotting
    plt.ion()