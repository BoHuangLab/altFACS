import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def combineGates(df: pd.DataFrame, gate1: str, gate1: str):
    '''
    Combine boolean 'gate' columns on annotated dataframe.
    
    Parameters:
    df: pd.DataFrame
    FACS data.
    
    gate1: str
    Name of gate1 column. Assumes a wavelength followed by a '+', e.g. 405nm+
    
    gate2: str
    Name of gate2 column. Assumes a wavelength followed by a '+', e.g. 488nm+
    
    
    Returns:
    df: pd.DataFrame
    FACS data with new columns for the combined gates. e.g '405nm_neg_488nm_neg'.
    
    '''
  
    assert gate1 in df.columns
    assert gate2 in df.columns
    
    #If there is no + at the end of the input string
    if gate1[-1] != '+':
        gate1 = gate1 + '+'
    
    if gate2[-1] != '+':
        gate2 = gate2 + '+'
           
    double_neg = ~df[gate1] & ~df[gate2]
    c1_pos     =  df[gate1] & ~df[gate2]
    c2_pos     = ~df[gate1] &  df[gate2]
    double_pos =  df[gate1] &  df[gate2]
    
    #handle gate or channel inputs
    channel1=gate1.replace('+', '', 1)
    channel2=gate2.replace('+', '', 1)
    
    n_n = channel1+"_neg_"+channel2+"_neg"
    p_n = channel1+"_pos_"+channel2+"_neg"
    n_p = channel1+"_neg_"+channel2+"_pos"
    p_p = channel1+"_pos_"+channel2+"_pos"
    
    df.loc[:, n_n] = double_neg
    df.loc[:, p_n] = c1_pos
    df.loc[:, n_p] = c2_pos
    df.loc[:, p_p] = double_pos
    
    return df


def hitRate(df, double_neg_col, c1_pos_col, c2_pos_col, double_pos_col):
    '''
    Calculate the hit rate (%); double_pos / (double_pos + c1_pos) *100, 
    and the false detection rate; c2_pos / (double_neg + c2_pos) *100.
    
    Parameters:
    df: pd.DataFrame
    FACS data.
    
    double_neg_col, c1_pos_col, c2_pos_col, double_pos_col:str
    The names of columns in df containing the combined gating information. c1 is channel1, c2 is channel2.
    
    
    Returns:
    HR:
    Hit Rate.
    
    FDR:
    False Detection Rate.
    
    '''

    #Calculate Hit Rate 
    HR = (df[double_pos_col]/(df[double_pos_col]+df[c1_pos_col]))*100

    #Calculate False Detection Rate
    FDR = (df[c2_pos_col]/(df[double_neg_col]+df[c2_pos_col]))*100

    #Calculate False Negative Rate
        #This is just the inverse of HR (no need to calculate)
        #FNR = 100-HR

    return HR, FDR


def countPlot(counts: pd.DataFrame, stat='HR', **kwargs) -> plt.Figure:
    '''
    Plot (and save) bar graphs comparing experiment to controls
    
    Parameters:
    counts: pd.DataFrame
    A dataframe with stats in different columns e.g. HR, or FDR.
    
    stat: str
    
    
    Optional Parameters:
    plot:
    
    title:
    
    width:
    
    con_color:
    
    exp_color:
    
    legend:
    
    save:
    
    '''
    
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
    mean_counts = counts.groupby(by=['landing_pad', 'condition'])[stat].mean().reset_index()
    std_counts = counts.groupby(by=['landing_pad', 'condition'])[stat].std().reset_index()

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