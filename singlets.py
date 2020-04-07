import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#This is a problem
from alternativeFACS.alternativeFACS.helpers.density  import *

def singletThreshold(data: pd.DataFrame, singlet_quantile, verbose=True)->float:
    '''Return the singlet ratio for a given quantile.'''
    
    assert 'FSC-A' in data.columns
    assert 'FSC-H' in data.columns

    x = data['FSC-A']
    y = data['FSC-H']
    
    ratio = y / x
    
    singlet_threshold = ratio.quantile(singlet_quantile)
    
    if verbose:
            print('The singlet threshold is', singlet_threshold)
            
    return singlet_threshold


def singletPlot(data: pd.DataFrame, singlet_threshold, **kwargs):
    '''Plot events above and below the singlet Threshold'''
    
    assert 'FSC-A' in data.columns
    assert 'FSC-H' in data.columns
    
    #Get **kwargs
    plot          = kwargs.get('plot', True)
    linecolour    = kwargs.get('linecolour', 'magenta')
    xlabel        = kwargs.get('xlabel', 'Forward Scatter Area')
    ylabel        = kwargs.get('ylabel', 'Forward Scatter Height')
    title         = kwargs.get('title', 'singletPlot_figure')
    size          = kwargs.get('size', 3)
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
    '''Add boolean Singlet-Gate indicating events above the singlet ratio.'''
    
    assert 'FSC-A' in data.columns
    assert 'FSC-H' in data.columns
    
    #Get **kwargs
    verbose           = kwargs.get('verbose', True)
    
    x = data['FSC-A']
    y = data['FSC-H']
    
    data.loc[:, 'Singlet+'] = (y/x)>singlet_threshold
    
    singlets = data[data['Singlet+']].copy()
    
    ##Count scatter_gated_events
    singlet_gated_events = len(singlets)
    
    if verbose:
        print('Singlet gated events =',singlet_gated_events) 
            
    return data