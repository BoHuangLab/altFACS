import sys
import unittest

import numpy as np
import pandas as pd

from altFACS.autocontrol import *

# Generate test DataFrame
test_df   = pd.DataFrame()

#Set the random seed to get a reproducible set of pseudorandom data
np.random.seed(1)

#Generate random jitter
jitter = np.random.rand(1000)

# Generate test DataFrame
test_df   = pd.DataFrame()
test_df.loc[:,'FSC-A']    = np.random.normal(50, 10, 1000)
test_df.loc[:,'FSC-H']    = test_df.loc[:,'FSC-A'] * (jitter + 0.95)

test_df.loc[:,'SSC-A']    = np.random.normal(50, 10, 1000)

test_df.loc[:,'405nm']    = np.random.normal(50, 10, 1000)
test_df.loc[:,'488nm']    = np.random.normal(50, 10, 1000)
test_df.loc[:,'564nm']    = np.random.normal(50, 50, 1000) # Add a fluorescence channel outside the 0-100 limits

expected_event_gating = [1000, 676, 533, 506]

class TestAutocontrol(unittest.TestCase):

    def test_processControl(self):
        # Run processControl with no kwargs
        singlet_threshold, poly, event_gating, singlets = processControl(test_df)
        
        # Check event gating
        self.assertTrue(event_gating.equals(expected_event_gating), "For this data set the events should match the expected gating.")
    
# Test edge cases
# There should be an error message if the upper and lower bounds are swapped by mistake

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)