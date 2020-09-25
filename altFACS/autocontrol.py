import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from altFACS.saturation  import *
from altFACS.density  import *
from altFACS.contours import *
from altFACS.singlets import *

def processControl(control: pd.DataFrame, **kwargs):
    '''determine and present scatter and singlet gates based on control data'''
    
    #Get **kwargs
    limit_dict = kwargs.get('limit_dict', None)
    plot       = kwargs.get('plot', False)
    verbose    = kwargs.get('verbose', True)
    save       = kwargs.get('save', False)
    savepath   = kwargs.get('savepath', './')
    
    singlet_quantile  = kwargs.get('singlet_quantile', 0.05)

    assert 0 < singlet_quantile < 1

    #Define plot settings
    plot_settings = {'plot': plot, 'save': save, 'savepath': savepath}

    # Step [1] - Mask saturation

    #Count total events
    total_events = len(control)

    #Check there are events to process
    if total_events <= 0:
        raise ValueError('There are no events to analyse. Check the input DataFrame.')
        return

    #Plot raw events
    plot_settings['title'] = 'step1_raw_events'
    densityScatterPlot(control, 'FSC-A', 'SSC-A', **plot_settings);
    plt.title('Raw Events');
    plt.show()

    #Load limit_dict. - Temporary
    if limit_dict is None:
        test_data_dir  = r"C:/Users/David Brown/Documents/PythonScripts_New/FACS/alternativeFACS/tests/"
        test_data_name = "example_18bit_limit_dict.json"

        with open(test_data_dir+test_data_name, 'r') as json_file:
            limit_dict = json.load(json_file)

    mask = tagSaturation(control, limit_dict, verbose=False)

    # Awkwardly plot
    mask[mask.Saturated].plot('FSC-A', 'SSC-A', kind='scatter', c='b', s=1, alpha=0.1);
    densityScatterPlot(mask[~mask.Saturated], 'FSC-A', 'SSC-A');
    plt.title('Mask Saturated Events');
    plt.show()

    # Drop Saturated
    unsaturated = mask.drop(mask[mask.Saturated].index)

    ##Count unsaturated
    unsaturated_events = len(unsaturated)

    if total_events <=0:
        raise ValueError('There are no unsaturated events to analyse. Check the limit dictionary.')
        return

    if verbose:
        print('Control has',unsaturated_events, ' unsaturated events')
        percent_unsaturated = unsaturated_events/ total_events * 100
        print(round(percent_unsaturated, 2),'% of total events remaining')

    ## Get contours
    poly = getContours(unsaturated, 'FSC-A', 'SSC-A', **plot_settings);
    plt.close()

    ## contourPlot
    plot_settings['title'] = 'step2_unsaturated_events'
    contourPlot(unsaturated, 'FSC-A', 'SSC-A', poly, **plot_settings)
    plt.title('Unsaturated Events');
    plt.show()

    ## Add scatter gate
    scatterGate(unsaturated, poly, verbose=True)

    ## Get scatter gated events
    scatter = unsaturated[unsaturated['Scatter+']].copy()

    ## Set transparancy by scatter gate
    alpha_dict = {True:1, False: 0.05}

    # Map alpha values onto 'Scatter+'
    transparencies = list(unsaturated['Scatter+'].map(alpha_dict))

    ringcolor = 'magenta'
    polyfill  = None

    # Plot to show scatter gating
    densityScatterPlot(unsaturated, 'FSC-A', 'SSC-A', alphas=transparencies)
    #Define polygon
    poly = Polygon(poly.xy, edgecolor = ringcolor, fill=polyfill)

    plt.gca().add_patch(poly);
    plt.title('Scatter Gated Events');
    plt.show()

    ##Count scatter_gated_events
    scatter_gated_events = len(scatter)

    if scatter_gated_events <= 0:
        raise ValueError('There are no events within the scatter gate. Check your contour and nbins values.')
        return

    if verbose:
        print('Control has',scatter_gated_events, ' scatter gated events')
        percent_scatter_gated = scatter_gated_events / total_events * 100
        print(round(percent_scatter_gated, 2),'% of total events remaining')

    #Plot scatter gate events on new axis
    densityScatterPlot(scatter, 'FSC-A', 'FSC-H', **plot_settings)
    plt.title('Scatter Gated Events');
    plt.show()

    ## Get singlet threshold
    singlet_threshold = singletThreshold(scatter, singlet_quantile)

    ## Gate singlets
    singletGate(scatter, singlet_threshold)

    ## Set transparancy by scatter gate
    alpha_dict = {True:1, False: 0.1}

    # Map alpha values onto 'Scatter+'
    transparencies = list(scatter['Singlet+'].map(alpha_dict))

    #Plot singlets
    densityScatterPlot(scatter, 'FSC-A', 'FSC-H', alphas=transparencies)

    linecolour='magenta'

    x=scatter['FSC-A']

    x=list(x.sort_values().reset_index(drop=True))

    xp_min = x[0]-1000
    xp_max = x[-1]+1000
    yp_min = singlet_threshold*xp_min
    yp_max = singlet_threshold*xp_max

    # draw threshold line
    plt.plot([xp_min, xp_max], [yp_min, yp_max], c = linecolour);
    plt.title('Singlet Events');
    plt.show()


    # Get singlets
    singlets = scatter[scatter["Singlet+"]].copy()

    # Count singlet events
    singlet_events = len(singlets)

    if singlet_events <= 0:
        raise ValueError('There are no events within the singlet gate. Check your singlet_q value.')
        return

    if verbose:
        print('Control has',singlet_events, ' singlet events')
        percent_singlet_gated = singlet_events / total_events * 100
        print(round(percent_singlet_gated, 2),'% of total events remaining')

    #Combine event counts into list
    event_gating = [total_events, unsaturated_events, scatter_gated_events, singlet_events]

    return singlet_threshold, poly, event_gating, singlets
