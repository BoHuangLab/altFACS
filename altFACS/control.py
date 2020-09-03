import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from altFACS.saturation  import *
from altFACS.density  import *
from altFACS.contours import *
from altFACS.singlets import *

def processControl(control: pd.DataFrame, limit_dict: dict, **kwargs):
    '''determine scatter and singlet gates based on control data
    
    Parameters:
    control: pd.DataFrame
    A control sample from this experiment. This should have the fewest perturbations and the least dead cells.
    
    limit_dict: dict
    A dictionary defining the minimum and maximum values for each channels. 
    This will be used to remove saturation, by excluding events outside this set of limits.
    Events outside the limits in any channel will be excluded from further analysis in all channels.
    
    Optional Parameters:
    plot: Boolean (True/False)
    Would you like to see plots in the notebook
    
    square: Boolean (True/False)
    Would you like to fix the xy aspect ratio to 1. 
    Square plots are the prefered presentation style for line fitting.
    
    verbose: Boolean (True/False)
    Would you like the events counts to be printed out?
    
    save: Boolean (True/False)
    Would you like the plots to be saved?
    
    savepath: str
    Where would you like the plots to be saved?
    
    singlet_quantile: float (Between 0 and 1)
    
    Returns:
    singlet_threshold:
    The 
    
    poly: plt.patches.Poly
    The polygon gate, intended to contain living cells.
    
    event_gating:
    A list of the number of events at each step
    0. total_events 
    1. unsaturated_events
    2. scatter_gated_events
    3. singlet_events  
    
    singlets: pd.DataFrame
    Events passing all of gating critera, intended to represent distinct living cells
    
    
    '''
    
    #Get **kwargs
    plot       = kwargs.get('plot', False)
    square     = kwargs.get('square', False)
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
    unsaturated = mask.dropna().copy() #explicit copy to avoid SettingWithCopyWarning
    
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
    scatter = unsaturated[unsaturated['Scatter+']].copy() #explicit copy to avoid SettingWithCopyWarning
    
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
    singlets = unsaturated[unsaturated["Singlet+"]].copy() #explicit copy to avoid SettingWithCopyWarning
    
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