import sys
import pandas as pd

#Mask channel
def maskChannelSaturation(df, channel, lower, upper):
    '''replace channel values below lower or above upper with NaN'''

    #Is the value above the lower threshold?  
    return df[channel].mask(~df[channel].between(lower, upper, inclusive = False))

#Iterate through channels
def maskSaturation(df: pd.DataFrame, **kwargs):
    '''replace values outside channel limits with NaN'''
    
    #Get **kwargs
    verbose    = kwargs.get('verbose', False)
    limit_dict = kwargs.get('limit_dict', {})
    FACS_channels = kwargs.get('FACS_channels', ['FSC-A', 'FSC-H', 'FSC-W', 'SSC-A'])
    fluorescence_channels = kwargs.get('fluorescence_channels', ['405nm', '488nm', '564nm', '646nm'])
    
    if verbose:
        print('Input events =', len(df))

    #Use pd.DataFrame.copy() otherwise you will generate a view which will get overwritten
    mask = df.copy()

    for channel in df.columns:
        if channel in FACS_channels + fluorescence_channels:
        
            if verbose:
                print('Removing',channel, 'saturation')

            #Retrive channel specific limits from dictionary, default to 0, 262144 = 18-bit range
            limits = limit_dict.get(channel, {'lower_limit': 0, 'upper_limit': 262144})
            
            lower = limits['lower_limit']
            upper = limits['upper_limit']
            
            #Mask events not between the upper and lower limits
            mask[channel] = maskChannelSaturation(mask, channel, lower, upper)
    
    if verbose:
        print('Unsaturated events =', len(mask.dropna()))

    return mask