import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import gaussian_kde as kde
from matplotlib.colors import Normalize
from matplotlib import cm

def densityScatterPlot(df: pd.DataFrame, x_channel: str, y_channel: str, **kwargs):
    '''
    function to generate publication quality 2D-density plots from FACS data
    
    Parameters:
    df: pd.DataFrame
    A dataframe containing your x and y values
    
    x_channel: str
    The name of the column in df containing x values.
    
    y_channel: str
    The name of the column in df containing y values.
    
    
    Optional Parameters:
    plot: bool
    Should a graph be plotted? If no, you can just save it directly, with save=True.
    
    ax:
    This allows densityScatterPlot to be called as a subplot.    
    
    title: str
    What would you like to title your graph. Default = densityScatter_figure.

    xlabel: str
    What would you like to label your x_axis? Default = x_channel.
    
    ylabel: str
    What would you like to label your y_axis? Default = y_channel.
    
    cmap: str
    Which color map would you like to use to show the density of points? Default = jet
    
    alphas: 0-1
    How transparent would you like the points?
    
    size: int?
    How large would you like the points?
    
    square: bool
    Would you like your plot in the square format?
   
    save: bool
    Would you like to save the figure? Default = False.
    
    savepath: str
    Where would you like to save the figure?
    
    
    '''
    
    #Get **kwargs
    plot      = kwargs.get('plot', True)
    ax        = kwargs.get('ax', plt.gca())
    title     = kwargs.get('title', 'densityScatter_figure')
    xlabel    = kwargs.get('xlabel', x_channel)
    ylabel    = kwargs.get('ylabel', y_channel)
    cmap      = kwargs.get('cmap', 'jet')
    alphas    = kwargs.get('alphas', None)
    size      = kwargs.get('size', 1)
    square    = kwargs.get('square', False)
    save      = kwargs.get('save', False)
    savepath  = kwargs.get('savepath', './')
    
    x = df[x_channel]
    y = df[y_channel]
    
    #Calculate density
    densObj = kde( [x, y] )

    vals = densObj.evaluate( [x, y] )

    colors = np.zeros( (len( vals ),3) )
    norm = Normalize( vmin=vals.min(), vmax=vals.max() )

    # Optionally set transparency of points based on a list of alpha values.
    if alphas is None:
        # Convert look up colormap to a list of RGB values for each point.
        colors = [cm.ScalarMappable( norm=norm, cmap=cmap).to_rgba(val) for val in vals]

    else:
        # Convert look up colormap to a list of RGBA values for each point.
        colors = [cm.ScalarMappable( norm=norm, cmap=cmap).to_rgba(val, alpha) for val, alpha in zip(vals, alphas)]

    if plot:
        ax.scatter( x, y, color=colors, s=size)
        ax.set_xlabel(xlabel);
        ax.set_ylabel(ylabel);

    else:
        plt.ioff()
        ax.scatter( x, y, color=colors, s=size)
        ax.set_xlabel(xlabel);
        ax.set_ylabel(ylabel);
        
    if square:
        plt.axis('square')
        ax.set_aspect('equal');
        plt.ticklabel_format(style='sci', scilimits=(0,0));
        
    if save:
        plt.tight_layout()
        plt.savefig(savepath+title)
        
    if plot==False:
        plt.close()
        
    #Restore interactive plotting
    plt.ion()