#!/usr/bin/env python3
import pandas as pd
import numpy as np

def ɸ(self, n=None):
    if n is None:
        # Reverse the series if there is no n value given
        return self[::-1]
    else:
        indices = np.arange(len(self))
        new_indices = indices - n
        n = new_indices % len(self)
        shifted_values = self.values.take(n)
        return pd.Series(shifted_values)
    
# Add the function to the pd.Series class
pd.Series.ɸ = ɸ

# Example usage
ser = pd.Series([1, 2, 3, 4, 5])

print(ser.ɸ(1).to_list())  # Output: [5, 1, 2, 3, 4]
print(ser.ɸ(2).to_list())  # Output: [4, 5, 1, 2, 3]
print(ser.ɸ(10).to_list()) # Output: [1, 2, 3, 4, 5]
print(ser.ɸ().to_list())   # Output: [5, 4, 3, 2, 1]