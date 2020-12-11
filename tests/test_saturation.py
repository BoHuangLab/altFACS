import sys
import unittest

import numpy as np
import pandas as pd

from altFACS.saturation import *

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

# Define expected outputs as pd.DataFrame
expected_mask_df = pd.DataFrame()
expected_mask_df.loc[:,'Channel-A'] = channel_A_mask
expected_mask_df.loc[:,'Channel-B'] = channel_B_mask

class TestSaturation(unittest.TestCase):

    def test_maskChannelSaturation(self):
        mask = maskChannelSaturation(df=test_df, channel = 'Channel-A', lower = 3, upper = 7)
        self.assertTrue(mask.equals(channel_A_mask), "Channel values at or beyond the upper or lower limits should be masked.")

    def test_maskSaturation(self):
        mask = maskSaturation(df=test_df, limit_dict=test_dict, verbose=False)
        self.assertTrue(mask.equals(expected_mask_df), "Values at or beyond the limits for that channel should be masked.")

# Test edge cases
# There should be an error message if the upper and lower bounds are swapped by mistake

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)