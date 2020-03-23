import sys
import pandas as pd
import matplotlib.pyplot as plt

##Make a generic plot function.
def overlayPlot(landing_pad_df: pd.DataFrame, x_channel: str, y_channel: str, **kwargs):
    '''function to generate a plot comparing mean signal across a number of bins'''
    
    #Get **kwargs
    plot      = kwargs.get('plot', True)
    title     = kwargs.get('title', 'overlayPlot_figure.pdf')
    con_color = kwargs.get('con_color', 'lightgrey') 
    exp_color = kwargs.get('exp_color', 'green')
    x_label   = kwargs.get('x_label', x_channel)
    y_label   = kwargs.get('y_label', y_channel)
    save      = kwargs.get('save', False)
    
    fig, ax = plt.subplots()
    
    if plot==False:
        plt.ioff()

    control_data = landing_pad_df[landing_pad_df.condition.eq('control')]
    control_data.plot(ax=ax, x=x_channel, y=y_channel, kind='scatter', c='lightgrey', alpha =0.1)

    experiment_data = landing_pad_df[landing_pad_df.condition.eq('experiment')]
    experiment_data.plot(ax=ax, x=x_channel, y=y_channel, kind='scatter', c='green', alpha =0.1)

    colors = {'control':'grey', 'experiment':'green'}

    #Bin data into 22 bins
    landing_pad_df.loc[:,'bin'] = pd.cut(landing_pad_df[x_channel], list(range(-1000, 10000, 500)))

    #Group by bin
    landing_pad_df = landing_pad_df.groupby(by=['landing_pad', 'condition','bin']).mean().reset_index()
    landing_pad_df

    grouped = landing_pad_df.groupby(by='condition')
    for key, group in grouped:
        group.plot(ax=ax, kind='line', x=x_channel, y=y_channel, label=key, color=colors[key])

    #Label Plot
    plt.xlabel(x_label);
    plt.ylabel(y_label);
    
    if save:
        plt.savefig(title)
    
    if plot==False:
        plt.close()
    else:
        plt.show()