import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from altFACS.density  import *

def singletThreshold(data: pd.DataFrame, singlet_quantile: float, verbose=True)->float:
    '''
    Return the singlet ratio for a given quantile.
    Intended to help distinguish and exclude flow cytometry events containing more than one cell.
    
    Parameters:
    data: pd.DataFrame
    Must contain columns labelled 'FSC-A' and 'FSC-H'
    
    singlet_quantile:float (0-1)
    What fraction of events would you like to exclude? 
    The higher the fraction, the more stringent, but the fewer events will be left.
    
    verbose:
    Would you like to print the calculated singlet threshold?
    
    
    Returns:
    singlet_threshold
    
    
    To Do:
    Add options for other singlet gating methods.
    
    
    '''
    
    assert 'FSC-A' in data.columns
    assert 'FSC-H' in data.columns
    assert 0 < singlet_quantile < 1

    x = data['FSC-A']
    y = data['FSC-H']
    
    ratio = y / x
    
    singlet_threshold = ratio.quantile(singlet_quantile)
    
    if verbose:
            print('The singlet threshold is', singlet_threshold)
            
    return singlet_threshold


def singletPlot(data: pd.DataFrame, singlet_threshold: float, **kwargs):
    '''
    Plot events above and below the singlet Threshold.
    
    
    Parameters:
    data: pd.DataFrame
    Must contain columns labelled 'FSC-A' and 'FSC-H'
    
    singlet_threshold: float
    Intended to accept the singlet_threshold value output by singletThreshold()
    
    Optional Parameters:
    plot: Boolean (True/False)
    Do you want to see the plots?
    
    linecolour: str
    Color of the threshold line
    
    xlabel: str
    
    ylabel: str
    
    title: str
    
    s: float
    Marker size
    
    doublet_color: str
    Color of markers below threshold
    
    doublet_alpha: float
    Transparency of markers below threshold
    
    save: Boolean (True/False)
    Do you want to save the plots?
    
    savepath: str
    Where do you want to save the plots?
    
    
    
    '''
    
    assert 'FSC-A' in data.columns
    assert 'FSC-H' in data.columns
    
    #Get **kwargs
    plot          = kwargs.get('plot', True)
    linecolour    = kwargs.get('linecolour', 'magenta')
    xlabel        = kwargs.get('xlabel', 'FSC-A')
    ylabel        = kwargs.get('ylabel', 'FSC-H')
    title         = kwargs.get('title', 'singletPlot_figure')
    s             = kwargs.get('s', 3)
    doublet_color = kwargs.get('doublet_color', 'blue')
    doublet_alpha = kwargs.get('doublet_alpha', 0.1)
    save          = kwargs.get('save', False)
    savepath      = kwargs.get('savepath', './')
    
    x = data['FSC-A']
    y = data['FSC-H']
    
    ratio = y / x
    
    doublets = data[ratio<=singlet_threshold]
    singlets = data[ratio>singlet_threshold]

    if plot:
        doublets.plot(x='FSC-A', y='FSC-H', kind='scatter', alpha=doublet_alpha, s=size, c=doublet_color);
        densityScatterPlot(singlets, 'FSC-A', 'FSC-H');
        
        x=list(x.sort_values().reset_index(drop=True))
    
        xp_min = x[0]-1000
        xp_max = x[-1]+1000
        yp_min = singlet_threshold*xp_min
        yp_max = singlet_threshold*xp_max
        
        # draw diagonal line from (70, 90) to (90, 200)
        plt.plot([xp_min, xp_max], [yp_min, yp_max], c = linecolour)
        
        #Label Plot
        plt.xlabel(xlabel);
        plt.ylabel(ylabel);
        
    else:
        plt.ioff()
        doublets.plot(x='FSC-A', y='FSC-H', kind='scatter', alpha=doublet_alpha, s=size, c=doublet_color);
        densityScatterPlot(singlets, 'FSC-A', 'FSC-H');
        
        x=list(x.sort_values().reset_index(drop=True))
        
        xp_min = x[0]-1000
        xp_max = x[-1]+1000
        yp_min = singlet_threshold*xp_min
        yp_max = singlet_threshold*xp_max
        
        # draw diagonal line from (70, 90) to (90, 200)
        plt.plot([xp_min, xp_max], [yp_min, yp_max], c = linecolour)
        
        #Label Plot
        plt.xlabel(xlabel);
        plt.ylabel(ylabel);

    if save:
        plt.tight_layout()
        plt.savefig(savepath+title)
        
    if plot==False:
        plt.close()
        
    #Restore interactive plotting
    plt.ion()

    
def singletGate(data: pd.DataFrame, singlet_threshold: float, **kwargs):
    '''
    Add boolean Singlet-Gate indicating events above the singlet ratio.
    
   
    Parameters:
    data: pd.DataFrame
    Must contain columns labelled 'FSC-A' and 'FSC-H'
    
    singlet_threshold: float
    Intended to accept the singlet_threshold value output by singletThreshold()
    
    Optional Parameters:
    verbose: Boolean (True/False)
    Would you like the number of Singlet gated events to be printed?
    
    
    Returns:
    data: pd.DataFrame
    The original DateFrame with an additional column 'Singlet+'.
    
    
    '''
    
    assert 'FSC-A' in data.columns
    assert 'FSC-H' in data.columns
    
    #Get **kwargs
    verbose           = kwargs.get('verbose', True)
    
    x = data['FSC-A']
    y = data['FSC-H']
    
    data.loc[:, 'Singlet+'] = (y/x) > singlet_threshold
    
    # This is just to calculate the number in hand
    singlets = data[data['Singlet+']].copy()
    
    ##Count scatter_gated_events
    singlet_gated_events = len(singlets)
    
    if verbose:
        print('Singlet gated events =',singlet_gated_events) 
            
    return data