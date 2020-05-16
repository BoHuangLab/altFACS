import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from alternativeFACS.alternativeFACS.helpers.saturation  import *
from alternativeFACS.alternativeFACS.helpers.density  import *
from alternativeFACS.alternativeFACS.helpers.contours import *
from alternativeFACS.alternativeFACS.helpers.singlets import *

def processControl(control: pd.DataFrame, limit_dict: dict, **kwargs):
    '''determine scatter and singlet gates based on control data'''
    
    #Get **kwargs
    plot       = kwargs.get('plot', False)
    verbose    = kwargs.get('verbose', True)
    save       = kwargs.get('save', False)
    savepath   = kwargs.get('savepath', './')
    
    singlet_quantile  = kwargs.get('singlet_quantile', 0.05)
    
    assert 0 < singlet_quantile < 1
    
    #Count total events
    total_events = len(control)
    
    if total_events <=0:
        print('There are no events to analyse. Check the input DataFrame.')
        return
    
    if plot:
        #Plot raw events
        plt.figure(1)
        kwargs['title'] = 'step1_raw_events'
        densityScatterPlot(control, 'FSC-A', 'SSC-A', **kwargs);
        plt.title('Raw Events');

    mask = maskSaturation(control, limit_dict, **kwargs)
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
    plt.figure()
    poly = getContours(unsaturated, 'FSC-A', 'SSC-A', **kwargs);
    plt.close()

    if plot:
        ## contourPlot
        plt.figure(2)
        kwargs['title'] = 'step2_unsaturated_events'
        contourPlot(unsaturated, 'FSC-A', 'SSC-A', poly, **kwargs)
        plt.title('Unsaturated Events');
    
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

    if plot:
        #Plot singlets
        plt.figure(3)
        kwargs['title'] = 'step3_singlet_events'
        singletPlot(scatter, singlet_threshold, **kwargs);
        plt.title('Singlet Plot');
    
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