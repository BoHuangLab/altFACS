"""
Distributions

The Huang Lab uses flow cytometry to investigate interactions between split fluorescent protein fragments. 
This module contains functions to resample distributions and quantifiy fold changes in FACS data.

Functions:

Requirements:

"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy import stats
from scipy import optimize

def resample(data1: pd.DataFrame, data2: pd.DataFrame, channel: str, bins: list):
    """
    Correct data2 distribution by resampling to correct for data1 distribtion.
    
    Parameters:
    data1: pd.DataFrame
    
    data2: pd.DataFrame
    
    channel: str
    Column name of the values for resampling.
    Should be present in data1 and data2
    
    bins: list
    
    
    Returns:
    resampled: pd.DataFrame    
    
    """
    
    #add bins to the dataframe
    data1.loc[:,'bin'] = pd.cut(data1[channel], bins)
    data2.loc[:,'bin'] = pd.cut(data2[channel], bins)

    #Group by bin
    data1_counts = data1['bin'].value_counts().sort_index().reset_index()
    data2_counts = data2['bin'].value_counts().sort_index().reset_index()

    #Normalise bins
    data1_counts.loc[:,'percent'] = data1_counts.loc[:,'bin'] / data1_counts.loc[:,'bin'].sum() * 100
    data2_counts.loc[:,'percent'] = data2_counts.loc[:,'bin'] / data2_counts.loc[:,'bin'].sum() * 100

    #Subtract control bins
    estimated_counts = data2_counts['percent'].subtract(data1_counts['percent'])

    #Exclude negatives
    estimated_counts = estimated_counts.clip(0,np.inf)
    
    ## re-normalise - is this needed? -yes
    renormalised = estimated_counts / estimated_counts.sum() *100
    
    data2_counts.loc[:, 'goal percentage'] = renormalised 
    data2_counts.loc[:, 'weight'] =  data2_counts.loc[:, 'goal percentage'] / data2_counts.loc[:, 'percent']
    
    #But it has to be less than it is now. - normalise weights to range 0-1
    weight_min   = data2_counts.loc[:, 'weight'].min()
    weight_max   = data2_counts.loc[:, 'weight'].max()
    weight_range = weight_max - weight_min

    #Divide without NaNs
    data2_counts.loc[:, 'frac'] = data2_counts.loc[:, 'weight'].divide(weight_range, fill_value=0)
    
    #Initialise list
    resampled = list()
    
    #group data
    grouped = data2.groupby(by='bin')

    for n, group in enumerate(grouped):
        group_bin = group[0]
        data      = group[1]

        resampled.append(data.sample(frac=data2_counts.loc[n, 'frac'], random_state=0))
    
    #Regenerate DataFrame
    resampled = pd.concat(resampled)
    
    return resampled


def distributionCorrection(df, channel):
    """
    Resample file pairs in a dataframe.
    
    df: pd.DataFrame
    
    channel: str
    Column name of the values for resampling.
    
    
    Returns:
    estimated_true_positives: pd.DataFrame
    
    
    To Do:
    Make a more generic function, or at least pull out hardcoded variables
    
    """

    #Initialise list 
    estimated_true_positives = list()

        #Step 1. - loop through architectures

    for LP in df['Architecture'].unique():

        #Step 2. - calculate control and experimental distribution
        control    = df[df.Architecture.eq(LP) &
                        df.Bait.eq('Control')]

        experiment = df[df.Architecture.eq(LP) & 
                        df.Bait.ne('Control')]

        #Step 3. - estimate distribution of true positives
        resampled = resample(control, experiment, channel, bins)

        #Step 4. - retrieve downsampled data
        estimated_true_positives.append(resampled)

    estimated_true_positives = pd.concat(estimated_true_positives, ignore_index=True)

    return estimated_true_positives