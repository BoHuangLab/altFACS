import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def setThresholds(control, **kwargs):
    '''
    process a control input to output singlets, a scatter gate, thresholds and event counts.
    '''
    
    #Get **kwargs
    plots      = kwargs.get('plots', False)
    verbose    = kwargs.get('verbose', True)
    contour    = kwargs.get('contour', 2)
    nbins      = kwargs.get('nbins', 300)
    edgecolour = kwargs.get('edgecolour', 'magenta')
    singlet_q  = kwargs.get('singlet_q', 0.05)
    
    #Assertions
    #control must be a pandas DataFrame
    assert type(control) == pd.core.frame.DataFrame
    
    #'control' must have 'FSC-A', 'SSC-A' and 'FSC-H' channels
    required_channels = ['FSC-A', 'SSC-A', 'FSC-H', 'MCherry-A', 'FITC-A', 'APC-A'] #Why should the control have these - 
    assert all(item in control.columns for item in required_channels)
    
    #Count total events
    total_events = len(control)
    
    if total_events <=0:
        print('There are no events to analyse. Check the input DataFrame.')
        return
    
    if plots:
        plt.ion()
        if verbose:
            print('Generating Figure 1')

        #Plots
        plt.figure(1)
        densityScatterPlot(control['FSC-A'], control['SSC-A']);
        #Label Plot
        

    ##Itentify saturation
    masked = maskSaturation(control, limit_dict);
    ##Remove saturation
    unsaturated = masked.dropna()
    
    ##Count unsaturated
    unsaturated_events = len(unsaturated)
    
    if total_events <=0:
        print('There are no unsaturated events to analyse. Check the limit dictionary.')
        return
    
    if verbose:
        print('Control has',unsaturated_events, ' unsaturated events')
        percent_unsaturated = unsaturated_events/ total_events * 100
        print(round(percent_unsaturated, 2),'% of total events remaining')
    
    #Generate density scatter gate
    #Define contour gate
    plt.figure(2)
    #I don't know how to turn this figure off
    poly = contourGate(unsaturated['FSC-A'], unsaturated['SSC-A'], contour=contour, nbins=nbins, plot=plots);
    
    if plots:
        plt.ion()
        if verbose:
            print('Generating Figure 3')
        plt.figure(3)
        densityScatterPlot(unsaturated['FSC-A'], unsaturated['SSC-A']);
        #Overlay "gate"
        plt.gca().add_patch(poly);
        #Label Plot
        plt.xlabel('Forward Scatter');
        plt.ylabel('Side Scatter');
        
    ##Scatter Gate Control
    coords = np.array(unsaturated[['FSC-A', 'SSC-A']])

    p = path.Path(poly.get_xy())

    #Detect gated events
    unsaturated.loc[:, "Scatter Gate"] = p.contains_points(coords)
    scatter = unsaturated[unsaturated['Scatter Gate']]
    
    ##Count scatter_gated_events
    scatter_gated_events = len(scatter)
    
    if scatter_gated_events <= 0:
        print('There are no events within the scatter gate. Check your contour and nbins values.')
        return
    
    if verbose:
        print('Control has',scatter_gated_events, ' scatter gated events')
        percent_scatter_gated = scatter_gated_events / total_events * 100
        print(round(percent_scatter_gated, 2),'% of total events remaining')
    
    #Define the singlet gate
    x = scatter['FSC-A']
    y = scatter['FSC-H']
    
    ratio = y / x
    singlet_threshold = ratio.quantile(singlet_q)
    
    if verbose:
        print('The singlet threshold is', singlet_threshold)

    if plots:
        print('Generating Figure 4')
        plt.figure(4)
    
        plt.scatter(x[ratio<=singlet_threshold], y[ratio<=singlet_threshold], alpha=0.1, s=3, c='blue');
        densityScatterPlot(x[ratio>singlet_threshold], y[ratio>singlet_threshold]);

        x=list(x.sort_values().reset_index(drop=True))

        xp_min = x[0]-1000
        xp_max = x[-1]+1000
        yp_min = singlet_threshold*xp_min
        yp_max = singlet_threshold*xp_max

        # draw diagonal line from (70, 90) to (90, 200)
        plt.plot([xp_min, xp_max], [yp_min, yp_max], 'magenta')

        #Label Plot
        plt.xlabel('Forward Scatter Area');
        plt.ylabel('Forward Scatter Height');
    
    #Singlet Gate Control
    singletGate(unsaturated, singlet_threshold)

    unsaturated.loc[:, "Singlets"] = unsaturated["Scatter Gate"] * unsaturated["Singlet Gate"]
    
    singlets = unsaturated[unsaturated["Singlets"]]
    
    #Count singlet events
    singlet_events = len(singlets)
    
    if singlet_events <= 0:
        print('There are no events within the singlet gate. Check your singlet_q value.')
        return
    
    if verbose:
        print('Control has',singlet_events, ' singlet events')
        percent_singlet_gated = singlet_events / total_events * 100
        print(round(percent_singlet_gated, 2),'% of total events remaining')
    
    ##Threshold Fluorescence channels
    
            #This could be done with a function to make it more generic and less repetitive.
    
    MCherry_autothresh = autothreshold(singlets, 'MCherry-A', 0.999)
    GFP_autothresh = autothreshold(singlets, 'FITC-A', 0.999)
    Halo_autothresh = autothreshold(singlets, 'APC-A', 0.999)

    #Quick check
    #print(MCherry_autothresh, GFP_autothresh, Halo_autothresh)

    #USE AUTOTHRESHOLDS ON THE CONTROL DATA SET
    singlets.loc[:, "mCherry+"] = singlets["MCherry-A"] > MCherry_autothresh
    singlets.loc[:, "GFP+"]     = singlets["FITC-A"]    > GFP_autothresh
    singlets.loc[:, "Halo+"]    = singlets["APC-A"]     > Halo_autothresh
    
    #Combine thresholds into a dictionary
    thresholds = dict({'Singlet':singlet_threshold, 'mCherry': MCherry_autothresh, 'GFP': GFP_autothresh, 'Halo': Halo_autothresh})
    
    #Combine event counts into list
    event_gating = [total_events, unsaturated_events, scatter_gated_events, singlet_events]
      
    return singlets, poly, thresholds, event_gating