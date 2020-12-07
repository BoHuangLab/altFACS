import unittest

import numpy as np
import pandas as pd

from altFACS.fluorescence  import *

# Define fixings

#Set the random seed to get a reproducible set of pseudorandom data
np.random.seed(1)

# Generate test DataFrame
test_df   = pd.DataFrame()
test_df.loc[:,'FSC-A']    = np.random.normal(0, 1, 1000)
test_df.loc[:,'405nm']    = np.random.normal(0, 1, 1000)
test_df.loc[:,'488nm']    = np.random.normal(0, 1, 1000)


class TestFlourescence(unittest.TestCase):
    
    def test_autothresholdChannel(self):
        
        # Use test_df to generate expected threshold with no kwargs
        threshold_405nm = autothresholdChannel(test_df, '405nm')
        self.assertEqual(threshold_405nm, test_df['405nm'].quantile(0.999), "Threshold should be set at 99.9th percentile .")
        
        # Use test_df to generate expected threshold with percentile kwarg
        test_percentile = 0.5
        threshold_405nm = autothresholdChannel(test_df, '405nm', percentile=test_percentile)
        self.assertEqual(threshold_405nm, test_df['405nm'].quantile(test_percentile), "Threshold should be set at 99.9th percentile .")
        
        # Use test_df to generate expected threshold with n_stdevs kwarg
        threshold_405nm = autothresholdChannel(test_df, '405nm', n_stdevs=1)
        self.assertEqual(threshold_405nm, test_df['405nm'].mean() + test_df['405nm'].std(), "Threshold should be set at mean+1*std .")

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)