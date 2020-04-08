import sys
import pandas as pd

#Mask channel
def maskChannelSaturation(df, channel, lower, upper):
    '''replace channel values below lower or above upper with NaN'''

    #Is the value above the lower threshold?  
    return df[channel].mask(~df[channel].between(lower, upper, inclusive = False))


#Iterate through channels
def maskSaturation(df: pd.DataFrame, limit_dict: dict, **kwargs):
    '''replace values outside channel limits with NaN'''
    
    #Get **kwargs
    verbose     = kwargs.get('verbose', True)
    
    if verbose:
        print('Input events =', len(df))

    #You have to use pd.DataFrame.copy() otherwise you will generate a view which will get overwritten
    mask = df.copy()

    for channel in df.columns:
        if channel in limit_dict.keys():
        
            if verbose:
                print('Removing',channel, 'saturation')

            #Retrive channel specific limits from dictionary
            lower = limit_dict[channel]['lower_limit']
            upper = limit_dict[channel]['upper_limit']

            #Mask events not between the upper and lower limits
            mask[channel] = maskChannelSaturation(mask, channel, lower, upper)
    
    if verbose:
        print('Unsaturated events =', len(mask.dropna()))

    return mask