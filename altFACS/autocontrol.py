import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from altFACS.saturation  import *
from altFACS.density  import *
from altFACS.contours import *
from altFACS.singlets import *

def processControl(control: pd.DataFrame, **kwargs):
    '''determine scatter and singlet gates based on control data'''
    
    #Get **kwargs
    limit_dict = kwargs.get('limit_dict', None)
    plot       = kwargs.get('plot', False)
    verbose    = kwargs.get('verbose', True)
    save       = kwargs.get('save', False)
    savepath   = kwargs.get('savepath', './')
    
    singlet_quantile  = kwargs.get('singlet_quantile', 0.05)
    
    assert 0 < singlet_quantile < 1
       
    #Define plot settings
    plot_settings = {plot, save, savepath} 
    
    # Step [1] - Mask saturation

    #Count total events
    total_events = len(control)
    
    #Check there are events to process
    if total_events <=0:
        print('There are no events to analyse. Check the input DataFrame.')
        return
    
    #Plot raw events
    kwargs['title'] = 'step1_raw_events'
    densityScatterPlot(control, 'FSC-A', 'SSC-A', **plot_settings);
    plt.title('Raw Events');
    plt.show()
        
    mask = maskSaturation(control, limit_dict, verbose)
    unsaturated = mask.dropna()
    
    ##Count unsaturated
    unsaturated_events = len(unsaturated)
    
    if total_events <=0:
        print('There are no unsaturated events to analyse. Check the limit dictionary.')
        return
    
    if verbose:
        print('Control has',unsaturated_events, ' unsaturated events')
        percent_unsaturated = unsaturated_events/ total_events * 100
        print(round(percent_unsaturated, 2),'% of total events remaining')

    ## Get contours
    poly = getContours(unsaturated, 'FSC-A', 'SSC-A', **plot_settings);
    plt.close()

    ## contourPlot
    kwargs['title'] = 'step2_unsaturated_events'
    contourPlot(unsaturated, 'FSC-A', 'SSC-A', poly, **plot_settings)
    plt.title('Unsaturated Events');
    plt.show()
    
    ## Add scatter gate 
    scatterGate(unsaturated, poly, verbose=True)
    
    ## Get scatter gated events
    scatter = unsaturated[unsaturated['Scatter+']].copy()
    
    ##Count scatter_gated_events
    scatter_gated_events = len(scatter)
    
    if scatter_gated_events <= 0:
        print('There are no events within the scatter gate. Check your contour and nbins values.')
        return
    
    if verbose:
        print('Control has',scatter_gated_events, ' scatter gated events')
        percent_scatter_gated = scatter_gated_events / total_events * 100
        print(round(percent_scatter_gated, 2),'% of total events remaining')

    ## Get singlet threshold
    singlet_threshold = singletThreshold(scatter, singlet_quantile)

    #Plot singlets
    kwargs['title'] = 'step3_singlet_events'
    singletPlot(scatter, singlet_threshold, **plot_settings);
    plt.title('Singlet Plot');
    plt.show()
    
    ## Gate singlets
    singletGate(unsaturated, singlet_threshold)
    
    # Get singlets
    singlets = unsaturated[unsaturated["Singlet+"]].copy()
    
    # Count singlet events
    singlet_events = len(singlets)
    
    if singlet_events <= 0:
        print('There are no events within the singlet gate. Check your singlet_q value.')
        return
    
    if verbose:
        print('Control has',singlet_events, ' singlet events')
        percent_singlet_gated = singlet_events / total_events * 100
        print(round(percent_singlet_gated, 2),'% of total events remaining')
    
    #Combine event counts into list
    event_gating = [total_events, unsaturated_events, scatter_gated_events, singlet_events]           
    
    return singlet_threshold, poly, event_gating, singlets