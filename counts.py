import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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