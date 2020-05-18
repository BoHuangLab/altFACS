import numpy as np
import pandas as pd
from altFACS.saturation  import *

# Generate test DataFrame
test_df   = pd.DataFrame()

test_df.loc[:,'Channel-A'] = np.arange(10)
test_df.loc[:,'Channel-B'] = np.arange(10)

# Generate test limit_dictionary
test_dict = {'Channel-A': {'lower_limit':3, 'upper_limit':7}, 
             'Channel-B': {'lower_limit':6, 'upper_limit':8}}

# Define nan
nan = np.nan

# Define expected outputs as pd.Series
channel_A_mask = pd.Series([nan, nan, nan, nan, 4.0, 5.0, 6.0, nan, nan, nan])
channel_B_mask = pd.Series([nan, nan, nan, nan, nan, nan, nan, 7.0, nan, nan])

# Define expected outpus as pd.DataFrame
expected_mask_df = pd.DataFrame()
expected_mask_df.loc[:,'Channel-A'] = channel_A_mask
expected_mask_df.loc[:,'Channel-B'] = channel_B_mask

def test_maskChannelSaturation():
    mask = maskChannelSaturation(df=test_df, channel = 'Channel-A', lower = 3, upper = 7)
    assert mask.equals(channel_A_mask)

def test_maskSaturation():
    mask = maskSaturation(df=test_df, limit_dict=test_dict)
    assert mask.equals(expected_mask_df)
    
# Test edge cases
# There should be an error message if the upper and lower bounds are swapped by mistake

if __name__ == "__main__":
    test_maskChannelSaturation()
    test_maskSaturation()
    print("Everything passed")