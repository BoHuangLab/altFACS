import unittest

import numpy as np
import pandas as pd

from altFACS.singlets  import *

#Correct threshold
_threshold = 0.9888554097049977

#Incorrect threshold
# _threshold = 0.4

#Set the random seed to get a reproducible set of pseudorandom data
np.random.seed(1)

#Generate random jitter
jitter = np.random.rand(1000)

# Generate test DataFrame
test_df   = pd.DataFrame()
test_df.loc[:,'FSC-A']    = np.arange(1000)
test_df.loc[:,'FSC-H']    = test_df.loc[:,'FSC-A'] * (jitter + 0.95)
test_df.loc[:,'ratio']    = test_df['FSC-H']/test_df['FSC-A']

test_df.loc[:, 'Singlet+']   = test_df['FSC-H']/test_df['FSC-A'] > _threshold

expected_singlets = test_df[test_df['Singlet+']]

class TestSinglets(unittest.TestCase):
    
    def test_singletThreshold(self):
        
        # Use test to generate expected threshold
        expected_threshold = singletThreshold(data=test_df, singlet_quantile=0.05, verbose=False)
        self.assertEqual(expected_threshold, _threshold, 
                         "For the test data, singlet quantile of 0.05 should give 0.9888554097049977 .")
        
    def test_singletGate(self):
        
        # Use test to determine singlets
        singlets = singletGate(data=test_df, singlet_threshold=_threshold, verbose=False)
        singlets = singlets[singlets['Singlet+']]
        self.assertTrue(expected_singlets.equals(singlets), 
                         "For the test data, singlets should equal the expected singlets .")

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)