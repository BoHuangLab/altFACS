import sys
import unittest

import numpy as np
import pandas as pd

from altFACS.counts import *

# Generate test DataFrame
test_df  = pd.DataFrame() 
test_df['405nm+'] = [False, False, True, True]
test_df['488nm+'] = [False, True, False, True]

# Define expected output
output_df = test_df.copy()
output_df['405nm_neg_488nm_neg'] = [True,  False, False, False]
output_df['405nm_pos_488nm_neg'] = [False, False, True,  True ]
output_df['405nm_neg_488nm_pos'] = [False, True,  False, True ]
output_df['405nm_pos_488nm_pos'] = [False, False, False, True ]

# Define aggregate for hitRate test
agg = output_df.count()

class TestCounts(unittest.TestCase):

    def test_combineGates(self):

        self.assertTrue((combineGates(test_df, '405nm+', '488nm+') == output_df).all(), "Gates should be combined as expected")

    def test_hitRate(self):
        
        HR, FDR = hitRate(agg, '405nm_neg_488nm_neg', '405nm_pos_488nm_neg', '405nm_neg_488nm_pos', '405nm_pos_488nm_pos')
        
        self.assertEqual(HR,  50.0, "With this input hit rate (%) should be 50.")
        self.assertEqual(FDR, 50.0, "With this input false detection rate (%) should be 50.")

# Test edge cases


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)