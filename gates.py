import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import gaussian_kde as kde
from matplotlib.colors import Normalize
from matplotlib import cm
from matplotlib.patches import Polygon
from matplotlib import path

def countPlot(counts: pd.DataFrame, stat='HR', **kwargs) -> plt.Figure:
    '''function to plot (and save) bar graphs comparing experiment to controls'''
    
    #Expects a dataframe with stats in different columns e.g. HR, or FDR
    
    #Get **kwargs
    plot      = kwargs.get('plot', True)
    title     = kwargs.get('title', 'countPlot_figure')
    width     = kwargs.get('width', 0.35)                   # the width of the bars
    con_color = kwargs.get('con_color', 'lightgrey') 
    exp_color = kwargs.get('exp_color', 'green')
    legend    = kwargs.get('legend', True)
    save      = kwargs.get('save', False)
    
    #Calculate mean and std
    mean_counts = counts.groupby(by=['landing_pad', 'condition']).mean().reset_index()
    std_counts = counts.groupby(by=['landing_pad', 'condition']).std().reset_index()

    ##Get labels
    labels = mean_counts.landing_pad.unique()
    
    #Get means
    control_mean_HR = mean_counts[mean_counts.condition.eq('control')][stat]
    experiment_mean_HR = mean_counts[mean_counts.condition.eq('experiment')][stat]
    
    #Get standard deviations
    control_std_HR = std_counts[mean_counts.condition.eq('control')][stat]
    experiment_std_HR = std_counts[mean_counts.condition.eq('experiment')][stat]
    
    #Generate two colour bar plot
    x = np.arange(len(labels))  # the label locations
    
    #Turn interactive plotting off
    plt.ioff()

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, control_mean_HR, width, label='control', yerr=control_std_HR, color=con_color)
    rects2 = ax.bar(x + width/2, experiment_mean_HR, width, label='experiment', yerr=experiment_std_HR, color=exp_color)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(stat+' (%)')
    #ax.set_title("mCherry -> Halo HitRate for different GFP&Spy Fusion Architectures")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    
    if legend:
        ax.legend()

    fig.tight_layout()
    
    if save:
        fig.savefig(title)
        
    if plot:
        plt.show(fig)
    else:
        plt.close(fig)
        
        
def contourGate(x, y, contour: int, **kwargs)->plt.Polygon:
    '''function to generate and return a contour polygon for gating'''
    
    #Get **kwargs
    nbins     = kwargs.get('nbins', 300)
    plot      = kwargs.get('plot', False)
    title     = kwargs.get('title', 'contourPlot_figure')
    edgecolor = kwargs.get('edgecolor', 'magenta')
    save      = kwargs.get('save', False)
    
    # Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
    k = kde([x,y])
    xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    
    if plot==False:
        plt.ioff()
    
    CS = plt.contour(xi, yi, zi.reshape(xi.shape));
    
    if save:
        fig.savefig(title)
    
    if plot==False:
        plt.close()
    else:
        plt.show()

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
    poly = Polygon(np.column_stack([xp, yp]), edgecolor="magenta", fill=False)
    
    return poly